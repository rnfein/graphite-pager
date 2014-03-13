from graphitepager.level import Level


class BaseNotifier(object):

    def __init__(self, storage):
        self._client = None
        self._storage = storage
        self._domain = self.__class__.__name__.replace('Notifier', '')
        self.group_notifications = False

    def notify(self, alert, alert_key, level, description, html_description):
        notified = self._storage.is_locked_for_domain_and_key(self._domain, alert_key)
        if level == Level.NOMINAL and notified:
            self._notify(alert, level, description, html_description, nominal=True)
            self._storage.remove_lock_for_domain_and_key(self._domain, alert_key)
        elif level in (Level.WARNING, Level.CRITICAL, Level.NO_DATA) and not notified:
            self._notify(alert, level, description, html_description, nominal=False)
            self._storage.set_lock_for_domain_and_key(self._domain, alert_key)

    def _notify(self, alert, level, description, html_description, nominal=None):
        pass


class BaseGroupNotifier(BaseNotifier):
    def __init__(self, storage):
        super(BaseGroupNotifier, self).__init__(storage)
        self.group_notifications = True

    def notify(self, notifications):
        to_send = []

        for notification in notifications:
            alert = notification[0]
            alert_key = notification[1]
            level = notification[2]
            description = notification[3]
            html_description = notification[4]

            notified = self._storage.is_locked_for_domain_and_key(self._domain, alert_key)
            if level == Level.NOMINAL and notified:
                to_send.append({
                    'nominal': True,
                    'alert': alert,
                    'alert_key': alert_key,
                    'level': level,
                    'description': description,
                    'html_description': html_description,
                })
                self._storage.remove_lock_for_domain_and_key(self._domain, alert_key)
            elif level in (Level.WARNING, Level.CRITICAL, Level.NO_DATA) and not notified:
                to_send.append({
                    'nominal': False,
                    'alert': alert,
                    'alert_key': alert_key,
                    'level': level,
                    'description': description,
                    'html_description': html_description,
                })
                self._storage.set_lock_for_domain_and_key(self._domain, alert_key)

        if to_send:
            self._notify(to_send)

    def _notify(self, notifications):
        pass
