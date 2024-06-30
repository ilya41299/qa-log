import json
from pathlib import Path
from config import options
import re
from log_file_stats import LogFileStats, RequestInfo
from config import files
import os
import pprint

RESULT_DIRECTORY = "./results"
regex = r"^(?P<ip>\S+).+?(?P<date>\[[\s\S]+?\])\s\"(?P<method>[GET|POST|PUT|DELETE|OPTIONS|HEAD]+)\s+(?P<url>\S+).+?\".+?(?P<status_code>\d{3}).+?(?P<duration>\d+)(?!.*\d)"

for file in files:
    log_file_stats = LogFileStats()
    with open(Path(options.filepath).joinpath(file)) as log_file:
        for line in log_file:
            match = re.match(regex, line)
            if match:
                log_file_stats.add_statistic(
                    RequestInfo(
                        ip=match.group("ip"),
                        date=match.group("date"),
                        method=match.group("method"),
                        url=match.group("url"),
                        duration=int(match.group("duration")),
                    )
                )
    log_statistic = log_file_stats.get_statistic()

    result_file_path = Path(RESULT_DIRECTORY).joinpath(f"result_{file}.json")
    os.makedirs(os.path.dirname(result_file_path), exist_ok=True)
    with open(result_file_path, "w") as result_file:
        json.dump(log_statistic, result_file, indent=4)

    print(result_file_path)
    pprint.pp(log_statistic)
