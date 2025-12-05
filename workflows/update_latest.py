from lk_weather import ReadMe, WeatherReport3h

if __name__ == "__main__":
    WeatherReport3h.list_latest_from_remote()
    WeatherReport3h.aggregate()
    ReadMe().build()
