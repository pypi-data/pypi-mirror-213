from request_pressure_tracker.notifiers.cloudwatch import CloudWatchNotifier
from request_pressure_tracker.trackers.memory import InMemoryWSGIPressureTracker
from request_pressure_tracker.wsgi_django.base import get_django_settings


class CloudWatchWSGIPressureTracker(InMemoryWSGIPressureTracker):
    """
    Cache-based tracker with cloudwatch notifier
    """

    def __init__(self, parent_application):
        super().__init__(
            parent_application,
            send_stats_every_seconds=get_django_settings('REQUEST_PRESSURE_TRACKER_NOTIFY_EVERY_SECONDS', default=10),
            target_duration_seconds=get_django_settings('REQUEST_PRESSURE_TRACKER_TARGET_DURATION', default=60),
            notifiers=[
                CloudWatchNotifier(
                    environment=get_django_settings('REQUEST_PRESSURE_TRACKER_CLOUDWATCH_ENVIRONMENT'),
                    aws_access_key=get_django_settings('REQUEST_PRESSURE_TRACKER_CLOUDWATCH_ACCESS_KEY'),
                    aws_secret_key=get_django_settings('REQUEST_PRESSURE_TRACKER_CLOUDWATCH_SECRET_KEY'),
                    aws_region=get_django_settings('REQUEST_PRESSURE_TRACKER_CLOUDWATCH_REGION'),
                )
            ],
        )
