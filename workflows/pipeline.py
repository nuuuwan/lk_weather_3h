from weather_lk import WeatherReport3h

if __name__ == "__main__":
    wr3_list = WeatherReport3h.list_latest_from_remote()
    for wr3 in wr3_list:
        print(wr3)
