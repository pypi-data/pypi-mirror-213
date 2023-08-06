import threading
from datetime import datetime, timedelta
from typing import Iterable, List

from request_pressure_tracker.notifiers.base import BaseNotifier
from request_pressure_tracker.trackers.base import BaseWSGIPressureTracker, PressureRecord


class InMemoryWSGIPressureTracker(BaseWSGIPressureTracker):
    def __init__(
        self, parent_application,
        target_duration_seconds: int = 60,
        send_stats_every_seconds: int = 10,
        notifiers: Iterable[BaseNotifier] = None,
    ):
        self.storage = threading.local()
        super().__init__(
            parent_application,
            target_duration_seconds=target_duration_seconds,
            send_stats_every_seconds=send_stats_every_seconds,
            notifiers=notifiers,
        )

    def check_cooldown(self) -> bool:
        return datetime.utcnow() > self.last_notified + timedelta(seconds=self.send_stats_every_seconds)

    def refresh_cooldown(self) -> None:
        self.storage.last_notified = datetime.utcnow()

    @property
    def last_notified(self):
        return getattr(
            self.storage,
            'last_notified',
            datetime.utcnow() - timedelta(seconds=self.send_stats_every_seconds + 1)
        )

    @last_notified.setter
    def last_notified(self, value):
        self.storage.last_notified = value

    def set_stats(self, value: List[PressureRecord]):
        self.storage.stats = value

    def get_stats(self) -> List[PressureRecord]:
        return getattr(self.storage, 'stats', [])
