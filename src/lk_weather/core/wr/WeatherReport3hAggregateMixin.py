import os

from utils import JSONFile, Log, Time, TimeFormat

log = Log("WeatherReport3h")


class WeatherReport3hAggregateMixin:
    @classmethod
    def write_alert_data(cls):
        alert_data = {
            "url_source": cls.URL_REMOTE,
            "url_structured": "https://raw.githubusercontent.com"
            + "/nuuuwan/lk_weather_3h/refs/heads/main/data/alert_data.json",
            "event": "weather_report_3h",
            "event_measures": ["rain_mm", "temp_c", "rh"],
        }

        event_data = {}
        for wr in cls.list_all():
            station_name = wr.station_name
            time_ut = wr.time_ut
            date_part = TimeFormat.DATE_ID.format(Time(time_ut))
            time_only_part = TimeFormat("%H%M").format(Time(time_ut))

            if station_name not in event_data:
                event_data[station_name] = {}
            if date_part not in event_data[station_name]:
                event_data[station_name][date_part] = {}
            event_data[station_name][date_part][time_only_part] = {
                "rain_mm": wr.rain_mm,
                "temp_c": wr.temp_c,
                "rh": wr.rh,
            }

        alert_data["event_data"] = event_data
        alert_data_path_path = os.path.join("data", "alert_data.json")
        alert_data_file = JSONFile(alert_data_path_path)
        alert_data_file.write(alert_data)
        log.info(f"Wrote {alert_data_file}")

    @classmethod
    def write_weather_stations(cls):
        wr_list = cls.list_all()
        id_to_name = {}
        place_idx = cls.get_place_idx()
        unknown_station_names = []
        for wr in wr_list:
            station_id = wr.station_id
            station_name = wr.station_name
            if station_name not in place_idx:
                unknown_station_names.append(station_name)
            id_to_name[station_id] = wr.station_name

        weather_stations_path = os.path.join("data", "weather_stations.json")
        weather_stations_file = JSONFile(weather_stations_path)
        weather_stations_file.write(id_to_name)
        log.info(f"Wrote {weather_stations_file}")

        if unknown_station_names:
            n_unknown = len(unknown_station_names)
            log.warning(f"⚠️ Found {n_unknown} unknown station names.")
            unknown_file_path = os.path.join(
                "data", "unknown_weather_stations.json"
            )
            unknown_file = JSONFile(unknown_file_path)
            unknown_file.write(unknown_station_names)
            log.info(f"Wrote {unknown_file}")
        else:
            log.info("✅ No unknown station names found.")

    @classmethod
    def get_place_idx(cls) -> dict[str, dict]:
        places_path = os.path.join("data", "static", "places.json")
        places_file = JSONFile(places_path)
        places_d_list = places_file.read()
        return {place_d["name"]: place_d for place_d in places_d_list}

    @classmethod
    def aggregate(cls):
        cls.write_weather_stations()
        cls.write_alert_data()
