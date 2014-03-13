from unittest import TestCase

from mock import MagicMock

from graphitepager.notifiers.proxy import NotifierProxy
from graphitepager.notifiers.pagerduty_notifier import PagerdutyNotifier


class TestNotifierProxy(TestCase):

    def setUp(self):
        self.proxy = NotifierProxy()

    def test_adding_notifier(self):
        args = range(5)
        notifier = MagicMock(PagerdutyNotifier)
        notifier.group_notifications = False
        self.proxy.add_notifier(notifier)

        self.proxy.notify(*args)

        notifier.notify.assert_called_once_with(*args)

    def test_adding_multiple_notifiers(self):
        args = range(5)
        notifier_1 = MagicMock(PagerdutyNotifier)
        notifier_2 = MagicMock(PagerdutyNotifier)
        notifier_1.group_notifications = False
        notifier_2.group_notifications = False
        self.proxy.add_notifier(notifier_1)
        self.proxy.add_notifier(notifier_2)

        self.proxy.notify(*args)

        notifier_1.notify.assert_called_once_with(*args)
        notifier_2.notify.assert_called_once_with(*args)
