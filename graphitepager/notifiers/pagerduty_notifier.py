import os
from pagerduty import PagerDuty

from graphitepager.level import Level
from graphitepager.notifiers.base import BaseNotifier


class PagerdutyNotifier(BaseNotifier):

    def __init__(self, storage):
        super(PagerdutyNotifier, self).__init__(storage)

        self.enabled = all(x in os.environ for x in ['PAGERDUTY_KEY'])
        if self.enabled:
            self._client = PagerDuty(os.getenv('PAGERDUTY_KEY'))

    def notify(self, alert, alert_key, level, description, html_description):
        service_key = None
        if alert.get('pagerduty_key', None) is not None:
            service_key = self._client.service_key
            self._client.service_key = alert.get('pagerduty_key', None)

        incident_key = self._storage.get_incident_key_for_alert_key(alert_key)
        if level != Level.NOMINAL:
            description = str(description)
            incident_key = self._client.trigger(incident_key=incident_key, description=description)
            self._storage.set_incident_key_for_alert_key(alert_key, incident_key)
        elif incident_key is not None:
            self._client.resolve(incident_key=incident_key)
            self._storage.remove_incident_for_alert_key(alert_key)

        if service_key:
            self._client.service_key = service_key
