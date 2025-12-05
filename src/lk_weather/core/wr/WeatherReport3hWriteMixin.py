import os
from dataclasses import asdict


class WeatherReport3hWriteMixin:
    def write(self) -> bool:
        if self.json_file.exists:
            return False
        os.makedirs(self.dir_data, exist_ok=True)
        os.makedirs(os.path.dirname(self.json_file_path), exist_ok=True)
        self.json_file.write(asdict(self))
        return True
