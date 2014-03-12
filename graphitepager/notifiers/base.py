from graphitepager.level import Level


class BaseNotifier(object):

    def __init__(self, client, storage):
        self._client = client
        self._storage = storage
        self._domain = self.__class__.__name__.replace('Notifier', '')

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
