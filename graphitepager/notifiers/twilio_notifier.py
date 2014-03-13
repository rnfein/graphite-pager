import os
from twilio.rest import TwilioRestClient

from graphitepager.notifiers.base import BaseNotifier


class TwilioNotifier(BaseNotifier):

    def __init__(self, storage):
        super(TwilioNotifier, self).__init__(storage)

        required = ['TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN', 'TWILIO_OUTGOING_NUMBER', 'NOTIFY_PHONE_NUMBER']
        self.enabled = all(x in os.environ for x in required)
        if self.enabled:
            sid = os.getenv('TWILIO_ACCOUNT_SID')
            token = os.getenv('TWILIO_AUTH_TOKEN')
            self._client = TwilioRestClient(sid, token)
            self._phone_number = os.environ.get('NOTIFY_PHONE_NUMBER', None)

    def _notify(self, alert, level, description, html_description, nominal=None):
        if nominal:
            return

        self._client.sms.messages.create(
            to=alert.get('phone_number', self._phone_number),
            from_=os.environ.get('TWILIO_OUTGOING_NUMBER', None),
            body=str(description),
        )
