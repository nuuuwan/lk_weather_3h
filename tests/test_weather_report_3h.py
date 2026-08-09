import unittest
from unittest.mock import MagicMock, patch

from lk_weather import WeatherReport3h
from selenium.common.exceptions import TimeoutException


class TestCase(unittest.TestCase):
    @patch("lk_weather.core.wr.WeatherReport3hRemoteMixin.time.sleep")
    def test_load_remote_page_retries_timeout(self, sleep):
        driver = MagicMock()
        driver.get.side_effect = [TimeoutException(), None]

        WeatherReport3h._load_remote_page(driver)

        self.assertEqual(driver.get.call_count, 2)
        sleep.assert_called_once_with(
            WeatherReport3h.PAGE_LOAD_RETRY_DELAY_SECONDS
        )

    @patch("lk_weather.core.wr.WeatherReport3hRemoteMixin.time.sleep")
    def test_load_remote_page_raises_after_attempts(self, sleep):
        driver = MagicMock()
        driver.get.side_effect = TimeoutException()

        with self.assertRaises(TimeoutException):
            WeatherReport3h._load_remote_page(driver)

        self.assertEqual(
            driver.get.call_count,
            WeatherReport3h.PAGE_LOAD_ATTEMPTS,
        )
        self.assertEqual(
            sleep.call_count,
            WeatherReport3h.PAGE_LOAD_ATTEMPTS - 1,
        )

    @unittest.skip("Skip remote test")
    def test_method(self):
        wr3_list = WeatherReport3h.list_latest_from_remote()
        self.assertGreater(len(wr3_list), 0)
