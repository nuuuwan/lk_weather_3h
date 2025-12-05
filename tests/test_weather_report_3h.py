import unittest

from weather_lk import WeatherReport3h


class TestCase(unittest.TestCase):
    @unittest.skip("Skip remote test")
    def test_method(self):
        wr3_list = WeatherReport3h.list_latest_from_remote()
        self.assertGreater(len(wr3_list), 0)
