from .connection import Function


class FeedCtrlConnection(Function):
    """"Connectivity for the feed control group to check the master feeds and its corresponding child feeds."""

    def __init__(self):
        super(FeedCtrlConnection, self).__init__()

    def add_event(self, event):
        """Add an event to the master database as well as the general cbor database.

        @:parameter event: The new cbor event to be added
        @:returns 1 if successful, -1 if any error occurred
        """
        return super().insert_event(event)

    def get_trusted(self, master_id):
        """Get a list of all trusted feed_ids.

        @:parameter master_id: The master id of the user
        @:returns -1 if any error occurred or returns a list containing all the trusted feed ids
        """
        return self._handler.get_trusted(master_id)

    def get_blocked(self, master_id):
        """Get a list of all blocked feed_ids.

        @:parameter master_id: The master id of the user
        @:returns -1 if any error occurred or returns a list containing all the blocked feed ids
        """
        return self._handler.get_blocked(master_id)

    def get_all_master_ids(self):
        """Get a list of all master feed_ids.

        @:returns -1 if any error occurred or returns a list containing all the master ids in the database.
        """
        return self._handler.get_all_master_ids()

    def get_all_master_ids_feed_ids(self, master_id):
        """Get a list of all feed_ids of one master feed id.

        @:parameter master_id: The master id of the user
        @:returns -1 if any error occurred or returns a list containing all the feed ids subscribed to one master
        """
        return self._handler.get_all_master_ids_feed_ids(master_id)

    def get_username(self, master_id):
        """Get username to feed id.

        @:parameter master_id: A master id of the user
        @:returns -1 if any error occurred or returns the currently set username.
        """
        return self._handler.get_username(master_id)

    def get_my_last_event(self):
        """Get last event posted by master feed.

        @:returns -1 if any error occurred or returns the last event posted by the master feed.
        """
        return self._handler.get_my_last_event()

    def get_host_master_id(self):
        """Retrieve the master id of the host.

        @:returns -1 if any error occurred or returns the host master id.
        """
        return self._handler.get_host_master_id()

    def get_radius(self):
        """Get radius of host.

        @:returns -1 if any error occurred or returns the currently set radius of the host feed.
        """
        return self._handler.get_radius()

    def get_master_id_from_feed(self, feed_id):
        """Get the master feedid to a feed.

        @:parameter feed_id: A feed id from which one would like to know the master feed id
        @:returns -1 if any error occurred or returns a master feed id
        """
        return self._handler.get_master_id_from_feed(feed_id)

    def get_application_name(self, feed_id):
        """Get name of application.

        @:parameter feed_id: A feed id from which one would like to know the application name
        @:returns -1 if any error occurred or returns the application name
        """
        return self._handler.get_application_name(feed_id)

    def get_feed_ids_from_application_in_master_id(self, master_id, application_name):
        """Get feed all feed ids corresponding to an application.

        @:parameter master_id: A master id
        @:parameter application_name: An application name
        @:returns -1 if any error occurred or returns a list of the feed ids corresponding to one application name.
        """
        return self._handler.get_feed_ids_from_application_in_master_id(master_id, application_name)

    def get_feed_ids_in_radius(self):
        """Get feed all feed ids in radius of master feed.

        @:returns -1 if any error occurred or returns a list of the feed ids inside the current radius.
        """
        return self._handler.get_feed_ids_in_radius()

    def set_feed_ids_radius(self, feed_id, radius):
        """Get feed radius of a feed id.

        @:parameter feed_id: A feed id to which we want to set the radius.
        @:parameter radius: The radius we want to change it to.
        """
        return self._handler.set_feed_ids_radius(feed_id, radius)
