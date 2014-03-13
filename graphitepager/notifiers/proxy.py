class NotifierProxy(object):

    def __init__(self):
        self._notifiers = []
        self._notifications = []

    def add_notifier(self, notifier):
        self._notifiers.append(notifier)

    def clear(self):
        self._notifications = []

    def notify(self, *args, **kwargs):
        self._notifications.append(args)

        for notifier in self._notifiers:
            if not notifier.group_notifications:
                notifier.notify(*args, **kwargs)

    def group_notify(self):
        for notifier in self._notifiers:
            if notifier.group_notifications:
                notifier.notify(self._notifications)
        self.clear()
