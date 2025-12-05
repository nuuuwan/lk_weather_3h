import os

from utils import JSONFile, Time, TimeFormat


class WeatherReport3hReadMixin:

    DIR_DATA = "data"
    DIR_DATA_WEATHER_REPORT = os.path.join(DIR_DATA, "wr")

    @property
    def dir_data(self) -> str:
        time_id = TimeFormat("%Y-%m-%d-%H%M").format(Time(self.time_ut))
        year = time_id[:4]
        year_and_month = time_id[:7]
        year_and_month_and_day = time_id[:10]
        return os.path.join(
            self.DIR_DATA_WEATHER_REPORT,
            year,
            year_and_month,
            year_and_month_and_day,
            time_id,
        )

    @property
    def json_file_path(self) -> str:
        return os.path.join(
            self.dir_data,
            f"{self.station_id:06d}.json",
        )

    @property
    def json_file(self) -> JSONFile:
        return JSONFile(self.json_file_path)

    @classmethod
    def __get_json_files__(cls):
        json_files = []
        for dirpath, _, filenames in os.walk(cls.DIR_DATA_WEATHER_REPORT):
            for filename in filenames:
                if filename.endswith(".json"):
                    json_files.append(
                        JSONFile(os.path.join(dirpath, filename))
                    )
        return json_files

    @classmethod
    def from_json_file(cls, json_file: JSONFile):
        return cls(**json_file.read())

    @classmethod
    def list_all(cls) -> list:
        return [
            cls.from_json_file(json_file)
            for json_file in cls.__get_json_files__()
        ]
