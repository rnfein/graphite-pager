import os
from twilio.rest import TwilioRestClient

from graphitepager.notifiers.base import BaseNotifier

class TwilioNotifier(BaseNotifier):

    def __init__(self, storage):
        super(TwilioNotifier, self).__init__(storage)

        self.enabled = all(x in os.environ for x in ['TWILIO_ACCOUNT_SID', 'NOTIFY_PHONE_NUMBER'])
        if self.enabled:
            sid = os.getenv('TWILIO_ACCOUNT_SID')
            token = os.getenv('TWILIO_AUTH_TOKEN')
            self._client = TwilioRestClient(sid, token)

    def _notify(self, alert, level, description, html_description, nominal=None):
        if nominal:
            return

        phone_number = os.environ.get('NOTIFY_PHONE_NUMBER', None)
        if alert.get('phone_number', None) is not None:
            phone_number = alert.get('phone_number', None)

        description = str(description)
        self._client.sms.messages.create(
            to=phone_number,
            from_=os.environ.get('TWILIO_OUTGOING_NUMBER', None),
            body=description,
        )
