from dataclasses import dataclass

from utils import Log

from lk_weather.core.wr.WeatherReport3hAggregateMixin import \
    WeatherReport3hAggregateMixin
from lk_weather.core.wr.WeatherReport3hReadMixin import \
    WeatherReport3hReadMixin
from lk_weather.core.wr.WeatherReport3hRemoteMixin import \
    WeatherReport3hRemoteMixin
from lk_weather.core.wr.WeatherReport3hWriteMixin import \
    WeatherReport3hWriteMixin

log = Log("WeatherReport3h")


@dataclass
class WeatherReport3h(
    WeatherReport3hRemoteMixin,
    WeatherReport3hReadMixin,
    WeatherReport3hWriteMixin,
    WeatherReport3hAggregateMixin,
):
    station_id: int
    station_name: str
    time_ut: int
    rain_mm: float
    temp_c: float
    rh: float

    @property
    def dew_point_c(self) -> float:
        """Calculate dew point temperature in Celsius using the
        Magnus-Tetens approximation.
        """
        a = 17.27
        b = 237.7  # degrees Celsius
        alpha = ((a * self.temp_c) / (b + self.temp_c)) + (self.rh / 100)
        dew_point = (b * alpha) / (a - alpha)
        return dew_point
