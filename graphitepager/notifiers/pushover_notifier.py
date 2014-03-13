import os
import requests

from graphitepager.level import Level
from graphitepager.notifiers.base import BaseNotifier


class PushoverNotifier(BaseNotifier):

    def __init__(self, storage):
        super(PushoverNotifier, self).__init__(storage)

        required = ['PUSHOVER_TOKEN', 'PUSHOVER_USER_KEY']
        self.enabled = all(x in os.environ for x in required)
        if self.enabled:
            self._client = requests.post
            self._pushover_key = os.environ.get('PUSHOVER_USER_KEY')
            self._url = 'https://api.pushover.net/1/messages.json'

            self._payload = {}
            self._payload['token'] = os.environ.get('PUSHOVER_TOKEN')

    def _notify(self, alert, level, description, html_description, nominal=None):
        payload = self._payload
        payload['user'] = alert.get('pushover_key', self._pushover_key)
        payload['message'] = str(description)
        payload['title'] = alert.name,
        payload['priority'] = self._level_to_priority(level)
        if alert.documentation_url():
            payload['url'] = alert.documentation_url()
            payload['url_title'] = 'Documentation'

        self._client(self._url, data=payload)

    def _level_to_priority(self, level):
        mapping = {
            Level.NOMINAL: -1,
            Level.NO_DATA: 0,
            Level.WARNING: 0,
            Level.CRITICAL: 1,
        }

        return mapping.get(level, 2)
