class BaseNotifier:
    """
    Base class to notify external service with metric request spent in internal queue
    """

    def __init__(self):
        pass

    def notify_pressure(self, pressure: float) -> None:
        """
        Push exact value of time spent in queue
        :param pressure: float, amount of time, worker spent processing requests comparing to total time
        """
        raise NotImplementedError
