import logging
import statistics
import threading
from datetime import datetime, timedelta

from django.core.cache import BaseCache, InvalidCacheBackendError, caches

from request_pressure_tracker.notifiers.base import BaseNotifier

logger = logging.getLogger('django.time_in_queue')


def notify_average(
        cache: BaseCache,
        average_cache_key: str,
        pressure: float,
):
    cache.set(average_cache_key, pressure)


def notify_values(
        cache: BaseCache,
        values_cache_key: str,
        metrics_lifespan: timedelta,
        pressure: float,
):
    now = datetime.utcnow()

    # todo: prevent parallel access
    metrics = cache.get(values_cache_key, default=[])

    if not isinstance(metrics, list) or not all(len(m) == 2 for m in metrics):
        logger.warning("Bad cached value: {}".format(metrics))
        metrics = []

    # filter out dead metrics
    metrics = [v for v in metrics if now - datetime.fromtimestamp(v[0]) < metrics_lifespan]

    metrics.append((now.timestamp(), pressure))

    cache.set(values_cache_key, metrics)


def get_average(cache: BaseCache, values_cache_key: str) -> float:
    metrics = cache.get(values_cache_key, default=[])
    if not isinstance(metrics, list) or not all(len(m) == 2 for m in metrics):
        logger.warning("Bad cached value: {}".format(metrics))
        # todo: what is better to use here?
        return 0

    return statistics.mean([m[1] for m in metrics])


def notify_django_cache_pressure(
        cache: BaseCache,
        average_value_cache_key: str,
        values_cache_key: str,
        metrics_lifespan: timedelta,
        pressure: float,
):
    notify_values(cache, values_cache_key, metrics_lifespan, pressure)
    average_pressure = get_average(cache, values_cache_key)
    notify_average(cache, average_value_cache_key, average_pressure)


class DjangoCacheNotifier(BaseNotifier):
    def __init__(
            self,
            cache_name: str = 'default',
            cache_key_prefix: str = 'request-pressure-metrics',
            metrics_lifespan: timedelta = timedelta(minutes=2)
    ):
        super().__init__()

        self.cache_name = cache_name
        self.cache_key_prefix = cache_key_prefix
        self.metrics_lifespan = metrics_lifespan

        self._first_notify = True
        self.initialized = True

    def get_cache(self) -> BaseCache:
        try:
            return caches[self.cache_name]
        except InvalidCacheBackendError:
            logger.warning('Bad cache {0} defined. Using default'.format(self.cache_name))
            return caches['default']

    def get_average_cache_key(self) -> str:
        return '{0}-average'.format(self.cache_key_prefix)

    def get_values_cache_key(self) -> str:
        return '{0}-values'.format(self.cache_key_prefix)

    def notify_pressure(self, pressure: float) -> None:
        if not self.initialized:
            return

        if self._first_notify:
            # clear cache keys during init to avoid all sort of incompatibilities
            cache = self.get_cache()
            cache.delete(self.get_average_cache_key())
            self._first_notify = False

        threading.Thread(
            target=notify_django_cache_pressure,
            args=[
                self.get_cache(), self.get_average_cache_key(), self.get_values_cache_key(),
                self.metrics_lifespan, pressure,
            ],
        ).start()
