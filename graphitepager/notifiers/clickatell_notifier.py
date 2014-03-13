import os
import requests

from graphitepager.notifiers.base import BaseNotifier


class ClickatellNotifier(BaseNotifier):

    def __init__(self, storage):
        super(ClickatellNotifier, self).__init__(storage)

        required = ['CLICKATELL_USERNAME', 'CLICKATELL_PASSWORD', 'CLICKATELL_API_ID', 'CLICKATELL_OUTGOING_NUMBER', 'NOTIFY_PHONE_NUMBER']
        self.enabled = all(x in os.environ for x in required)
        if self.enabled:
            self._client = requests.get
            self._phone_number = os.environ.get('NOTIFY_PHONE_NUMBER')
            self._url = "http://api.clickatell.com/http/sendmsg"

            self._payload = {}
            self._payload['user'] = os.environ.get('CLICKATELL_USERNAME')
            self._payload['password'] = os.environ.get('CLICKATELL_PASSWORD')
            self._payload['api_id'] = os.environ.get('CLICKATELL_API_ID')
            self._payload['from'] = os.environ.get('CLICKATELL_OUTGOING_NUMBER')

    def _notify(self, alert, level, description, html_description, nominal=None):
        if nominal:
            return

        payload = self._payload
        payload['to'] = alert.get('phone_number', self._phone_number)
        payload['text'] = str(description)
        self._client(self._url, params=payload)
