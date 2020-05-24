from ECT_FCTRL_DB.logStore.funcs.EventCreationTool import EventFactory  # noqa: F401


class EventCreationWrapper:

    def __init__(self, eventFactory):
        self._eventFactory = eventFactory

    def create_MASTER(self):
        return self._eventFactory.next_event('MASTER/MASTER', {})

    def create_trust(self, feed_id):
        return self._eventFactory.next_event('MASTER/Trust', {'feed_id': feed_id})

    def create_name(self, name):
        return self._eventFactory.next_event('MASTER/Name', {'name': name})

    def create_newFeed(self, feed_id, appName):
        return self._eventFactory.next_event('MASTER/NewFeed', {'feed_id': feed_id, 'app_name': appName})

    def create_block(self, feed_id):
        return self._eventFactory.next_event('MASTER/Block', {'feed_id': feed_id})

    def create_radius(self, radius):
        return self._eventFactory.next_event('MASTER/Radius', {'radius': radius})
