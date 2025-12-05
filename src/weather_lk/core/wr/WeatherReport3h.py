from dataclasses import dataclass

from utils import Log

from weather_lk.core.wr.WeatherReport3hAggregateMixin import \
    WeatherReport3hAggregateMixin
from weather_lk.core.wr.WeatherReport3hReadMixin import \
    WeatherReport3hReadMixin
from weather_lk.core.wr.WeatherReport3hRemoteMixin import \
    WeatherReport3hRemoteMixin
from weather_lk.core.wr.WeatherReport3hWriteMixin import \
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
