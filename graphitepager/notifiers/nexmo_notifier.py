import os
import requests

from graphitepager.notifiers.base import BaseNotifier


class NexmoNotifier(BaseNotifier):

    def __init__(self, storage):
        super(NexmoNotifier, self).__init__(storage)

        required = ['NEXMO_API_KEY', 'NEXMO_API_SECRET', 'NEXMO_OUTGOING_NUMBER', 'NOTIFY_PHONE_NUMBER']
        self.enabled = all(x in os.environ for x in required)
        if self.enabled:
            self._client = requests.post
            self._phone_number = os.environ.get('NOTIFY_PHONE_NUMBER')
            self._url = "https://rest.nexmo.com/sms/json"

            self._payload = {}
            self._payload['api_key'] = os.environ.get('NEXMO_API_KEY')
            self._payload['api_secret'] = os.environ.get('NEXMO_API_SECRET')
            self._payload['from'] = os.environ.get('NEXMO_OUTGOING_NUMBER')

    def _notify(self, alert, level, description, html_description, nominal=None):
        if nominal:
            return

        payload = self._payload
        payload['to'] = alert.get('phone_number', self._phone_number)
        payload['text'] = str(description)
        self._client(self._url, data=payload)
