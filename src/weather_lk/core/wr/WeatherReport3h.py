import os
import time
from dataclasses import asdict, dataclass
from typing import List

from selenium import webdriver
from selenium.webdriver.common.by import By
from utils import JSONFile, Log, Time, TimeFormat

log = Log("WeatherReport3h")


class WeatherReport3hRemoteMixin:
    URL_REMOTE = "https://www.meteo.gov.lk"

    @classmethod
    def list_latest_from_remote(cls) -> List["WeatherReport3h"]:

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)

        try:
            driver.get(cls.URL_REMOTE)
            time.sleep(2)

            three_hourly_button = driver.find_element(
                By.XPATH, "//button[contains(text(), '3 Hourly Data')]"
            )
            three_hourly_button.click()
            time.sleep(1)

            load_data_button = driver.find_element(
                By.XPATH, "//button[contains(text(), 'Load Data')]"
            )
            load_data_button.click()
            time.sleep(3)

            weather_reports = []
            table = driver.find_element(By.TAG_NAME, "table")

            rows = table.find_elements(By.TAG_NAME, "tr")[1:]

            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                col_text_list = [col.text for col in cols]
                if len(col_text_list) >= 6:
                    time_str = col_text_list[2].strip()
                    time_ut = TimeFormat("%Y-%m-%d %H%M").parse(time_str).ut
                    rain_mm_str = col_text_list[3].strip()
                    rain_mm = (
                        float(rain_mm_str)
                        if rain_mm_str not in ["", "TR"]
                        else 0.0
                    )
                    report = cls(
                        station_id=int(col_text_list[0].strip()),
                        station_name=col_text_list[1].strip(),
                        time_ut=time_ut,
                        rain_mm=rain_mm,
                        temp_c=float(col_text_list[4].strip() or 0),
                        rh=float(col_text_list[5].strip() or 0) / 100.0,
                    )

                    report.write()

                    weather_reports.append(report)

            return weather_reports

        finally:
            driver.quit()


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
    def from_json_file(cls, json_file: JSONFile) -> "WeatherReport3h":
        return cls(**json_file.read())

    @classmethod
    def list_all(cls) -> List["WeatherReport3h"]:
        return [
            cls.from_json_file(json_file)
            for json_file in cls.__get_json_files__()
        ]


class WeatherReport3hWriteMixin:
    def write(self) -> bool:
        if self.json_file.exists:
            return False
        os.makedirs(self.dir_data, exist_ok=True)
        os.makedirs(os.path.dirname(self.json_file_path), exist_ok=True)
        self.json_file.write(asdict(self))
        return True


@dataclass
class WeatherReport3h(
    WeatherReport3hRemoteMixin,
    WeatherReport3hReadMixin,
    WeatherReport3hWriteMixin,
):
    station_id: int
    station_name: str
    time_ut: int
    rain_mm: float
    temp_c: float
    rh: float
