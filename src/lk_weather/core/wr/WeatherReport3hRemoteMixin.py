import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from utils import TimeFormat


class WeatherReport3hRemoteMixin:
    URL_REMOTE = "https://www.meteo.gov.lk"

    @classmethod
    def list_latest_from_remote(cls) -> list:

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
                    rain_mm_str = col_text_list[3].strip().replace("..", ".")
                    rain_mm = (
                        float(rain_mm_str)
                        if rain_mm_str.lower() not in ["", "tr"]
                        else 0.0
                    )
                    temp_c_str = col_text_list[5].strip()
                    temp_c = float(temp_c_str)
                    report = cls(
                        station_id=int(col_text_list[0].strip()),
                        station_name=col_text_list[1].strip().title(),
                        time_ut=time_ut,
                        rain_mm=rain_mm,
                        temp_c=temp_c,
                        rh=float(col_text_list[6].strip() or 0) / 100.0,
                    )

                    report.write()

                    weather_reports.append(report)

            return weather_reports

        finally:
            driver.quit()
