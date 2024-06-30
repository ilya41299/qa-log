from dataclasses import dataclass


@dataclass
class RequestInfo:
    ip: str
    date: str
    method: str
    url: str
    duration: int


class LogFileStats:
    top_ips = dict()
    total_requests = 0
    total_stats = {
        "GET": 0,
        "POST": 0,
        "HEAD": 0,
        "PUT": 0,
        "OPTIONS": 0,
        "DELETE": 0,
    }
    top_longest: list[RequestInfo] = []

    def add_statistic(self, request_info: RequestInfo) -> None:
        self.total_requests += 1
        self.total_stats[request_info.method] += 1

        self.top_ips.setdefault(request_info.ip, 0)
        self.top_ips[request_info.ip] += 1

        if len(self.top_longest) < 3:
            self.top_longest.append(request_info)
            self.top_longest = sorted(
                self.top_longest, key=lambda x: x.duration, reverse=True
            )
        else:
            if request_info.duration > self.top_longest[-1].duration:
                self.top_longest.append(request_info)
                self.top_longest = sorted(
                    self.top_longest, key=lambda x: x.duration, reverse=True
                )[:3]

    def get_top_ips(self, number=3) -> dict[str:int]:
        return dict(
            sorted(self.top_ips.items(), reverse=True, key=lambda item: item[1])[
                :number
            ]
        )

    def get_statistic(self) -> dict:
        return {
            "top_ips": self.get_top_ips(),
            "top_longest": [
                {
                    "ip": request.ip,
                    "date": request.date,
                    "method": request.method,
                    "url": request.url,
                    "duration": request.duration,
                }
                for request in self.top_longest
            ],
            "total_stat": self.total_stats,
            "total_requests": self.total_requests,
        }
