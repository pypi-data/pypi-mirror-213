from datetime import timedelta

from request_pressure_tracker.notifiers.django_cache import DjangoCacheNotifier
from request_pressure_tracker.trackers.memory import InMemoryWSGIPressureTracker
from request_pressure_tracker.wsgi_django.base import get_django_settings


class DjangoCachePressureTracker(InMemoryWSGIPressureTracker):
    """
    Memory-based tracker with cache notifier
    """

    def __init__(self, parent_application):
        super().__init__(
            parent_application,
            send_stats_every_seconds=get_django_settings('REQUEST_PRESSURE_TRACKER_NOTIFY_EVERY_SECONDS', default=30),
            target_duration_seconds=get_django_settings('REQUEST_PRESSURE_TRACKER_TARGET_DURATION_SECONDS', default=2 * 60),
            notifiers=[
                DjangoCacheNotifier(
                    cache_name=get_django_settings('REQUEST_PRESSURE_TRACKER_NOTIFY_CACHE_NAME', default='unknown'),
                    cache_key_prefix=get_django_settings('REQUEST_PRESSURE_TRACKER_NOTIFY_CACHE_KEY_PREFIX',
                                                         default='request-pressure-metrics'),
                    metrics_lifespan=timedelta(
                        seconds=get_django_settings('REQUEST_PRESSURE_TRACKER_NOTIFY_METRICS_LIFESPAN_SECONDS',
                                                    default=120),
                    ),
                )
            ],
        )
