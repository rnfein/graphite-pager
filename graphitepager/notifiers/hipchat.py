from graphitepager.level import Level
from graphitepager.notifiers.base import BaseNotifier


class HipChatNotifier(BaseNotifier):

    def __init__(self, client, storage):
        super(HipChatNotifier, self).__init__(client, storage)
        self._rooms = set()

    def _notify(self, alert, level, description, html_description, nominal=None):
        colors = {
            Level.NOMINAL: 'green',
            Level.WARNING: 'yellow',
            Level.CRITICAL: 'red',
        }
        color = colors.get(level, 'red')

        description = str(html_description)
        self._notify_room_with_args(
            'Graphite-Pager',
            description,
            message_format='html',
            color=color,
        )

    def _notify_room_with_args(self, *args, **kwargs):
        for room in self._rooms:
            self._client.message_room(room, *args, **kwargs)

    def add_room(self, room):
        self._rooms.add(room)
