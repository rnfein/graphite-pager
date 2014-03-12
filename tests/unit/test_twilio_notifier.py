from unittest import TestCase

from mock import patch, MagicMock
from twilio.rest import TwilioRestClient
from twilio.rest.resources import Sms, SmsMessages


from graphitepager.notifiers.twilio_notifier import TwilioNotifier
from graphitepager.redis_storage import RedisStorage
from graphitepager.alerts import Alert
from graphitepager.level import Level


class TestTwilioNotifier(TestCase):

    def setUp(self):
        self.alert_key = 'ALERT KEY'
        self.description = 'ALERT DESCRIPTION'
        self.html_description = 'HTML ALERT DESCRIPTION'
        self.mock_redis_storage = MagicMock(RedisStorage)
        self.mock_twilio_client = MagicMock(TwilioRestClient)
        self.mock_twilio_sms = MagicMock(Sms)
        self.mock_twilio_sms_messages = MagicMock(SmsMessages)
        self.mock_alert = MagicMock(Alert)

        self.mock_twilio_client.sms = self.mock_twilio_sms
        self.mock_twilio_client.sms.messages = self.mock_twilio_sms_messages

        self.notifier = TwilioNotifier(self.mock_redis_storage)
        self.notifier._client = self.mock_twilio_client

    def test_should_not_notify_if_warning_and_already_notified(self):
        self.mock_redis_storage.is_locked_for_domain_and_key.return_value = True

        self.notifier.notify(self.mock_alert, self.alert_key, Level.WARNING, self.description, self.html_description)

        self.assertEqual(self.mock_twilio_client.mock_calls, [])

    def test_should_notify_resolved_if_nominal_and_had_notified(self):
        self.mock_redis_storage.is_locked_for_domain_and_key.return_value = True

        self.notifier.notify(self.mock_alert, self.alert_key, Level.NOMINAL, self.description, self.html_description)

        self.mock_redis_storage.is_locked_for_domain_and_key.assert_called_once_with(
            'Twilio', self.alert_key)
        self.assertEqual(self.mock_twilio_client.mock_calls, [])
        self.mock_redis_storage.remove_lock_for_domain_and_key.assert_called_once_with(
            'Twilio', self.alert_key)

    def test_should_notify_warning_if_had_not_notified_before(self):
        self.mock_redis_storage.is_locked_for_domain_and_key.return_value = False

        self.notifier.notify(self.mock_alert, self.alert_key, Level.WARNING, self.description, self.html_description)

        self.mock_twilio_client.sms.messages.create.assert_called_once_with(
            to=self.mock_alert.get('phone_number', None),
            from_=None,
            body=self.description
        )
        self.mock_redis_storage.set_lock_for_domain_and_key.assert_called_once_with(
            'Twilio', self.alert_key)

    def test_should_notify_critical_if_had_not_notified_before(self):
        self.mock_redis_storage.is_locked_for_domain_and_key.return_value = False

        self.notifier.notify(self.mock_alert, self.alert_key, Level.CRITICAL, self.description, self.html_description)

        self.mock_twilio_client.sms.messages.create.assert_called_once_with(
            to=self.mock_alert.get('phone_number', None),
            from_=None,
            body=self.description
        )
        self.mock_redis_storage.set_lock_for_domain_and_key.assert_called_once_with(
            'Twilio', self.alert_key)

    def test_should_notify_no_data_if_had_not_notified_before(self):
        self.mock_redis_storage.is_locked_for_domain_and_key.return_value = False

        self.notifier.notify(self.mock_alert, self.alert_key, Level.NO_DATA, self.description, self.html_description)

        self.mock_twilio_client.sms.messages.create.assert_called_once_with(
            to=self.mock_alert.get('phone_number', None),
            from_=None,
            body=self.description
        )
        self.mock_redis_storage.set_lock_for_domain_and_key.assert_called_once_with(
            'Twilio', self.alert_key)
