from .connection import Function


class FeedCtrlConnection(Function):
    """"Connectivity for the feed control group to check the master feeds and its corresponding child feeds."""

    def __init__(self):
        super(FeedCtrlConnection, self).__init__()

    def add_event(self, event):
        """Add an event to the master database as well as the general cbor database.

        Tested and works!"""
        return super().insert_event(event)

    def get_trusted(self, master_id):
        """Get an array of all trusted feed_ids.

        Tested and works!"""
        return self._handler.get_trusted(master_id)

    def get_blocked(self, master_id):
        """Get an array of all blocked feed_ids.

        Tested and works!"""
        return self._handler.get_blocked(master_id)

    def get_all_master_ids(self):
        """Get an array of all master feed_ids.

                Tested and works!"""
        return self._handler.get_all_master_ids()

    def get_all_master_ids_feed_ids(self, master_id):
        """Get an array of all feed_ids of one master feed id.

                Tested and works!"""
        return self._handler.get_all_master_ids_feed_ids(master_id)

    def get_username(self, master_id):
        """Get username to feed id.

                Tested and works!"""
        return self._handler.get_username(master_id)

    def get_my_last_event(self):
        """Get last event posted by master feed.

                Tested and works!"""
        return self._handler.get_my_last_event()

    def get_host_master_id(self):
        """Retrieve the master id of the host.

        Tested and works!"""
        return self._handler.get_host_master_id()

    def get_radius(self):
        """Get radius of host.

                Tested and works!"""
        return self._handler.get_radius()

    def get_master_id_from_feed(self, feed_id):
        """Get the master feedid to a feed.

                Tested and works!"""
        return self._handler.get_master_id_from_feed(feed_id)

    def get_application_name(self, feed_id):
        """Get name of application.

                Tested and works!"""
        return self._handler.get_application_name(feed_id)

    def get_feed_ids_from_application_in_master_id(self, master_id, application_name):
        """Get feed all feed ids corresponding to an application.

                Tested and works!"""
        return self._handler.get_feed_ids_from_application_in_master_id(master_id, application_name)

    def get_feed_ids_in_radius(self):
        """Get feed all feed ids in radius of master feed.

                Tested and works!"""
        return self._handler.get_feed_ids_in_radius()

    def set_feed_ids_radius(self, feed_id, radius):
        """Get feed radius of a feed id.

                Tested and works!"""
        return self._handler.set_feed_ids_radius(feed_id, radius)
