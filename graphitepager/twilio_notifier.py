from level import Level
import os


class TwilioNotifier(object):

    def __init__(self, client, storage):
        self._client = client
        self._storage = storage

    def notify(self, alert, alert_key, level, description, html_description):
        phone_number = os.getenv('NOTIFY_PHONE_NUMBER')
        if alert.get('phone_number', None) is not None:
            phone_number = alert.get('phone_number', None)

        domain = 'Twilio'
        notified = self._storage.is_locked_for_domain_and_key(domain, alert_key)
        if level == Level.NOMINAL and notified:
            self._storage.remove_lock_for_domain_and_key(domain, alert_key)
        elif level in (Level.WARNING, Level.CRITICAL, Level.NO_DATA) and not notified:
            description = str(description)
            self._client.sms.messages.create(
                to=phone_number,
                from_=os.getenv('TWILIO_OUTGOING_NUMBER'),
                body=description,
            )
            self._storage.set_lock_for_domain_and_key(domain, alert_key)