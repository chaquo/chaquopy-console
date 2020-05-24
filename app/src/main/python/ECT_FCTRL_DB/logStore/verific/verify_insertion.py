from ..appconn.feed_ctrl_connection import FeedCtrlConnection
from ..funcs.log import create_logger

logger = create_logger('Verification')


class Verification:
    def __init__(self):
        self._fcc = FeedCtrlConnection()
        self._hostid = self._fcc.get_host_master_id()

    """
    This method is used to check if a given incoming feed should be accepted or not.
    @:parameter feed_id: The feed_id to check.
    @:parameter app_name: The app_name for which will be checked in the radius.
    @:returns True if accepted or False if not.
    """
    def check_incoming(self, feed_id, app_name):
        if self._hostid is None:
            self._hostid = self._fcc.get_host_master_id()
        # If the given feed is a master feed we will always accept it.
        if app_name == 'MASTER':
            return True
        else:
            trusted = self._fcc.get_trusted(self._hostid)
            blocked = self._fcc.get_blocked(self._hostid)
            # check if the feedID is trusted and not blocked
            if feed_id in trusted and feed_id not in blocked:
                return True
            return self._check_in_radius(app_name)

    """
        This method is used to check if a given outgoing feed should be accepted or not.
        @:parameter feed_id: The feed_id to check.
        @:returns True if accepted or False if not.
        """
    def check_outgoing(self, feed_id):
        if self._hostid is None:
            self._hostid = self._fcc.get_host_master_id()
        if feed_id == self._hostid:
            return True
        # check if the feed_id is a master id.
        master = set(self._fcc.get_all_master_ids())
        blocked = set(self._fcc.get_blocked(self._hostid))
        if feed_id in master:
            return True
        # check if the feed_id is not blocked
        if feed_id in blocked:
            return False
        else:
            # check if the feed_id is trusted
            trusted = set(self._fcc.get_trusted(self._hostid))
            if feed_id in trusted:
                return True
            return self._check_in_radius(feed_id)

    """
    This method should not be used outside of the Verification class or unit tests.
    """
    def _check_in_radius(self, app_name):
        master_in_radius = self._fcc.get_feed_ids_in_radius()
        if master_in_radius is None:
            return False
        # check if the feed_id is inside the social radius
        for master in master_in_radius:
            feedIDs = self._fcc.get_trusted(master)
            if feedIDs is not None:
                for feed_id in feedIDs:
                    if app_name == self._fcc.get_application_name(feed_id):
                        return True
        return False
