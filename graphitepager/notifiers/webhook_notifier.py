import json
import os
import requests

from graphitepager.notifiers.base import BaseNotifier


class WebhookNotifier(BaseNotifier):

    def __init__(self, storage):
        super(WebhookNotifier, self).__init__(storage)

        self.enabled = all(x in os.environ for x in ['WEBHOOK_URL'])
        if self.enabled:
            self._client = requests.post
            self._url = os.environ.get('WEBHOOK_URL')

    def _notify(self, alert, level, description, html_description, nominal=None):
        self._client(alert.get('webhook_url', self._url), data=json.dumps({
            'name': alert.name,
            'level': level,
            'description': str(description),
            'documentation_url': alert.documentation_url(),
        }))
