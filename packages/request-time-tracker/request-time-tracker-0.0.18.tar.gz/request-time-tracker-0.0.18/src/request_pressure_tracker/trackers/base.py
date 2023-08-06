import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Iterable, List

from request_pressure_tracker.notifiers.base import BaseNotifier

logger = logging.getLogger('django.time_in_queue')


@dataclass
class PressureRecord:
    start: datetime
    duration: timedelta


class BaseWSGIPressureTracker:
    def __init__(
        self, parent_application,
        target_duration_seconds: int = 60,
        send_stats_every_seconds: int = 10,
        notifiers: Iterable[BaseNotifier] = None,
    ):
        self.parent_application = parent_application
        self.send_stats_every_seconds = send_stats_every_seconds
        self.notifiers = notifiers
        self.target_duration = timedelta(seconds=target_duration_seconds)
        self.set_stats([])

    def set_stats(self, value: List[PressureRecord]):
        raise NotImplementedError

    def get_stats(self) -> List[PressureRecord]:
        raise NotImplementedError

    def cleanup(self):
        stats = self.get_stats()
        while stats:
            pressure_record = stats[0]
            start, duration = pressure_record.start, pressure_record.duration
            if start + duration < datetime.utcnow() - self.target_duration:
                stats.pop(0)
                self.set_stats(stats)
            else:
                break

    def get_pressure(self) -> float:
        time_spent = timedelta(seconds=0)
        baseline = datetime.utcnow() - self.target_duration

        for e in reversed(self.get_stats()):
            request_start, request_duration = e.start, e.duration
            if request_start > baseline:
                time_spent += request_duration
            elif request_start + request_duration > baseline:
                time_spent += request_duration - (baseline - request_start)
            else:
                break

        return time_spent / self.target_duration

    def count_request(
            self,
            start: datetime,
            duration: timedelta,
    ):
        # optimization: do cleanup once per N requests
        self.cleanup()
        stats = self.get_stats()
        stats.append(PressureRecord(start, duration))
        self.set_stats(stats)

    def check_cooldown(self) -> bool:
        """
        check if we're ready to send notification again
        """
        raise NotImplementedError

    def refresh_cooldown(self) -> None:
        """
        update cooldown counter
        """
        raise NotImplementedError

    def __call__(self, environ: dict, start_response: callable):
        start_time = datetime.utcnow()
        response = self.parent_application(environ, start_response)
        duration = datetime.utcnow() - start_time
        self.count_request(start_time, duration)

        if self.check_cooldown():
            self.refresh_cooldown()
            for notifier in self.notifiers:
                notifier.notify_pressure(self.get_pressure())

        return response
