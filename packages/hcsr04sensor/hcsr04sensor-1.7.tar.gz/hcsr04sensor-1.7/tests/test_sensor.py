import math
import RPi.GPIO as GPIO
import unittest
from hcsr04sensor.sensor import Measurement

TRIG_PIN = 17
ECHO_PIN = 27
GPIO_MODE = GPIO.BCM


class TestHcsr04sensor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up GPIO mode for the entire test class
        GPIO.setmode(GPIO_MODE)

    @classmethod
    def tearDownClass(cls):
        # Clean up GPIO pins for the entire test class
        GPIO.cleanup((TRIG_PIN, ECHO_PIN))

    def setUp(self):
        # Create a Measurement instance with specific temperature and unit for each test method
        self.value = Measurement(TRIG_PIN, ECHO_PIN, 25, "metric", gpio_mode=GPIO_MODE)

    def test_measurement(self):
        """Test that object is being created properly."""
        value = Measurement(TRIG_PIN, ECHO_PIN, 25, "metric", gpio_mode=GPIO_MODE)
        value_defaults = Measurement(TRIG_PIN, ECHO_PIN)
        self.assertIsInstance(value, Measurement)
        self.assertEqual(value.trig_pin, TRIG_PIN)
        self.assertEqual(value.echo_pin, ECHO_PIN)
        self.assertEqual(value.temperature, 25)
        self.assertEqual(value.unit, "metric")
        self.assertEqual(value_defaults.trig_pin, TRIG_PIN)
        self.assertEqual(value_defaults.echo_pin, ECHO_PIN)
        self.assertEqual(value_defaults.temperature, 20)
        self.assertEqual(value_defaults.unit, "metric")

    def test_imperial_temperature_and_speed_of_sound(self):
        """Test that after Fahrenheit is converted to Celsius, speed of sound is calculated correctly."""
        value = Measurement(TRIG_PIN, ECHO_PIN, 68, "imperial", gpio_mode=GPIO_MODE)
        raw_measurement = value.raw_distance()
        speed_of_sound = 331.3 * math.sqrt(1 + (value.temperature / 273.15))
        self.assertAlmostEqual(value.temperature, 20.0016)
        self.assertEqual(value.unit, "imperial")
        self.assertIsInstance(raw_measurement, float)
        self.assertAlmostEqual(speed_of_sound, 343.21555930656075)

    def test_imperial_measurements(self):
        """Test that an imperial measurement is what you would expect with a precise raw_measurement."""
        value = Measurement(TRIG_PIN, ECHO_PIN, 68, "imperial", gpio_mode=GPIO_MODE)
        raw_measurement = 26.454564846
        hole_depth = 25
        imperial_distance = value.distance_imperial(raw_measurement)
        imperial_depth = value.depth_imperial(raw_measurement, hole_depth)
        self.assertIsInstance(imperial_distance, float)
        self.assertAlmostEqual(imperial_distance, 10.423098549324001)
        self.assertAlmostEqual(imperial_depth, 14.576901450675999)

    def test_metric_measurements(self):
        """Test that a metric measurement is what you would expect with a precise raw_measurement."""
        value = Measurement(TRIG_PIN, ECHO_PIN, 20, "metric", gpio_mode=GPIO_MODE)
        raw_measurement = 48.80804985408
        hole_depth = 72
        metric_distance = value.distance_metric(raw_measurement)
        metric_depth = value.depth_metric(raw_measurement, hole_depth)
        self.assertAlmostEqual(metric_distance, 48.80804985408)
        self.assertAlmostEqual(metric_depth, 23.191950145920003)

    def test_different_sample_size(self):
        """Test that a user defined sample_size works correctly."""
        value = Measurement(TRIG_PIN, ECHO_PIN, 20, "metric", gpio_mode=GPIO_MODE)
        raw_measurement1 = value.raw_distance(sample_size=1)
        raw_measurement2 = value.raw_distance(sample_size=4)
        raw_measurement3 = value.raw_distance(sample_size=11)
        self.assertIsInstance(raw_measurement1, float)
        self.assertIsInstance(raw_measurement2, float)
        self.assertIsInstance(raw_measurement3, float)

    def test_different_sample_wait(self):
        """Test that a user defined sample_wait time works correctly."""
        value = Measurement(TRIG_PIN, ECHO_PIN, 20, "metric", gpio_mode=GPIO_MODE)
        raw_measurement1 = value.raw_distance(sample_wait=0.3)
        raw_measurement2 = value.raw_distance(sample_wait=0.1)
        raw_measurement3 = value.raw_distance(sample_wait=0.03)
        raw_measurement4 = value.raw_distance(sample_wait=0.01)
        self.assertIsInstance(raw_measurement1, float)
        self.assertIsInstance(raw_measurement2, float)
        self.assertIsInstance(raw_measurement3, float)
        self.assertIsInstance(raw_measurement4, float)

    def test_basic_distance_bcm(self):
        """Test that float is returned with default, positive, and negative temperatures."""
        x = Measurement
        basic_reading = x.basic_distance(TRIG_PIN, ECHO_PIN)
        basic_reading2 = x.basic_distance(TRIG_PIN, ECHO_PIN, celsius=10)
        basic_reading3 = x.basic_distance(TRIG_PIN, ECHO_PIN, celsius=0)
        basic_reading4 = x.basic_distance(TRIG_PIN, ECHO_PIN, celsius=-100)
        self.assertIsInstance(basic_reading, float)
        self.assertIsInstance(basic_reading2, float)
        self.assertIsInstance(basic_reading3, float)
        self.assertIsInstance(basic_reading4, float)

    def test_raises_exception_unit(self):
        """Test that a ValueError is raised if the user passes an invalid unit type."""
        value = Measurement(TRIG_PIN, ECHO_PIN, unit="Fahrenheit")
        self.assertRaises(ValueError, value.raw_distance)

    def test_raises_exception_no_pulse(self):
        """Test that SystemError is raised if echo pulse is not received."""
        # Typically this error gets raised with a faulty cable.
        # Wrong echo pin simulates that condition.
        wrong_echo_pin = ECHO_PIN - 1
        value = Measurement(TRIG_PIN, wrong_echo_pin)
        self.assertRaises(SystemError, value.raw_distance)

    def test_depth(self):
        """Test the depth of a liquid."""
        value = Measurement(TRIG_PIN, ECHO_PIN, 20, "metric", gpio_mode=GPIO_MODE)
        raw_measurement = 48.80804985408
        hole_depth = 72
        metric_depth = value.depth(raw_measurement, hole_depth)
        self.assertAlmostEqual(metric_depth, 23.191950145920003)
        value2 = Measurement(TRIG_PIN, ECHO_PIN, 68, "imperial", gpio_mode=GPIO_MODE)
        hole_depth_inches = hole_depth * 0.394
        imperial_depth = value2.depth(raw_measurement, hole_depth_inches)
        self.assertAlmostEqual(imperial_depth, 9.137628357492481)

    def test_distance(self):
        """Test the distance measurement."""
        value = Measurement(TRIG_PIN, ECHO_PIN, 20, "metric", gpio_mode=GPIO_MODE)
        raw_measurement = 48.80804985408
        metric_distance = value.distance(raw_measurement)
        self.assertAlmostEqual(metric_distance, 48.80804985408)
        value2 = Measurement(TRIG_PIN, ECHO_PIN, 68, "imperial", gpio_mode=GPIO_MODE)
        imperial_distance = value2.distance(raw_measurement)
        self.assertAlmostEqual(imperial_distance, 19.23037164250752)

    def test_cylinder_volume_side(self):
        """Test the volume of liquid in a cylinder resting on its side."""
        value = Measurement(TRIG_PIN, ECHO_PIN, 20, "metric", gpio_mode=GPIO_MODE)
        depth = 20
        height = 120
        radius = 45

        cylinder_volume = value.cylinder_volume_side(depth, height, radius)
        self.assertAlmostEqual(cylinder_volume, 126.31926004538707)

        value2 = Measurement(TRIG_PIN, ECHO_PIN, 68, "imperial", gpio_mode=GPIO_MODE)
        depthi = 17
        heighti = 27
        radiusi = 18
        cylinder_volume_g = value2.cylinder_volume_side(depthi, heighti, radiusi)
        self.assertAlmostEqual(cylinder_volume_g, 55.28063419280857)

    def test_catch_runtime_errors(self):
        """Test that a RuntimeError is caught and printed when using metric system."""
        value = Measurement(TRIG_PIN, ECHO_PIN, 20, "metric", gpio_mode=GPIO_MODE)
        # Override the GPIO pin access to simulate a RuntimeError
        value.GPIO_TRIGGER = 9999
        with self.assertRaises(RuntimeError) as cm:
            value.raw_distance()
        self.assertEqual(
            str(cm.exception),
            "RuntimeError: Timeout occurred while waiting for measurement.",
        )

    def test_catch_runtime_errors_imperial(self):
        """Test that a RuntimeError is caught and printed when using imperial system."""
        value = Measurement(TRIG_PIN, ECHO_PIN, 68, "imperial", gpio_mode=GPIO_MODE)
        # Override the GPIO pin access to simulate a RuntimeError
        value.GPIO_TRIGGER = 9999
        with self.assertRaises(RuntimeError) as cm:
            value.raw_distance()
        self.assertEqual(
            str(cm.exception),
            "RuntimeError: Timeout occurred while waiting for measurement.",
        )


if __name__ == "__main__":
    unittest.main()
