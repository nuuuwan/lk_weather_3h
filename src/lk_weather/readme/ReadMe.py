from utils import File, Log, Time, TimeFormat

from lk_weather import WeatherReport3h

log = Log("ReadMe")


class ReadMe:
    PATH = "README.md"

    def get_lines_for_latest(self) -> list[str]:
        lines = []
        max_time_ut = WeatherReport3h.get_max_time_ut()
        time_str = TimeFormat.TIME.format(Time(max_time_ut))
        wr3_list = WeatherReport3h.list_latest_batch()
        lines.append("## Latest 3-hourly Weather Reports")
        lines.append("")
        lines.append(f"*{time_str}*")
        lines.append("")
        lines.append(
            "| Station ID | Station Name | Time (UT) | Rain (mm) | Temp (°C) | RH (%) |"  # noqa: E501
        )
        lines.append(
            "|-----------:|--------------|-----------|----------:|----------:|-------:|"  # noqa: E501
        )
        for wr3 in wr3_list:
            time_str = TimeFormat.TIME.format(Time(wr3.time_ut))
            lines.append(
                f"| {wr3.station_id} | {wr3.station_name} | "
                f"{time_str} | {wr3.rain_mm:.1f} | {wr3.temp_c:.1f} | {wr3.rh:.0%} |"  # noqa: E501
            )
        lines.append("")
        return lines

    def get_lines_for_header(self) -> list[str]:
        url_remote = WeatherReport3h.URL_REMOTE
        return [
            "# lk_weather_3h",
            "",
            "The Department of Meteorology of Sri Lanka",
            "publishes 3-hourly weather reports",
            f"at [{url_remote}]({url_remote}).",
            "This repository scrapes, stores and aggregates this data.",
            "",
        ]

    def get_lines(self) -> list[str]:
        return self.get_lines_for_header() + self.get_lines_for_latest()

    def build(self) -> None:
        lines = self.get_lines()
        readme_file = File(self.PATH)
        readme_file.write_lines(lines)
        log.info(f"Wrote {readme_file}")
