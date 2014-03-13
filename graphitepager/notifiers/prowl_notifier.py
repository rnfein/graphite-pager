import os
import requests

from graphitepager.level import Level
from graphitepager.notifiers.base import BaseNotifier


class ProwlNotifier(BaseNotifier):

    def __init__(self, storage):
        super(ProwlNotifier, self).__init__(storage)

        required = ['PROWL_API_KEY']
        self.enabled = all(x in os.environ for x in required)
        if self.enabled:
            self._client = requests.post
            self._url = 'https://api.prowlapp.com/publicapi/add'

            self._payload = {}
            self._payload['apikey'] = os.environ.get('PROWL_API_KEY')
            self._payload['application'] = os.environ.get('PROWL_APPLICATION', 'graphite-pager')
            if os.environ.get('PROWL_PROVIDERKEY', None) is not None:
                self._payload['providerkey'] = os.environ.get('PROWL_PROVIDERKEY', None)

    def _notify(self, alert, level, description, html_description, nominal=None):
        payload = self._payload
        payload['priority'] = self._level_to_priority(level)
        payload['event'] = alert.name,
        payload['description'] = str(description)
        if alert.documentation_url():
            payload['url'] = alert.documentation_url()

        self._client(self._url, data=payload)

    def _level_to_priority(self, level):
        mapping = {
            Level.NOMINAL: -1,
            Level.NO_DATA: 0,
            Level.WARNING: 1,
            Level.CRITICAL: 2,
        }

        return mapping.get(level, 2)
