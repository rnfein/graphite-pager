import os

from graphitepager.notifiers.base import BaseNotifier

class TwilioNotifier(BaseNotifier):

    def __init__(self, client, storage):
        super(TwilioNotifier, self).__init__(client, storage)

    def _notify(self, alert, level, description, html_description, nominal=None):
        if nominal:
            return

        phone_number = os.getenv('NOTIFY_PHONE_NUMBER')
        if alert.get('phone_number', None) is not None:
            phone_number = alert.get('phone_number', None)

        description = str(description)
        self._client.sms.messages.create(
            to=phone_number,
            from_=os.getenv('TWILIO_OUTGOING_NUMBER'),
            body=description,
        )
