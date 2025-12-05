from utils import File, Log

from lk_weather import WeatherReport3h

log = Log("ReadMe")


class ReadMe:
    PATH = "README.md"

    def get_lines(self) -> list[str]:
        url_remote = WeatherReport3h.URL_REMOTE
        return [
            "#lk_weather_3h",
            "",
            "The Department of Meteorology of Sri Lanka",
            "publishes 3-hourly weather reports",
            f"at [{url_remote}]({url_remote}).",
            "This repository scrapes, stores and aggregates this data.",
            "",
        ]

    def build(self) -> None:
        lines = self.get_lines()
        readme_file = File(self.PATH)
        readme_file.write_lines(lines)
        log.info(f"Wrote {readme_file}")
