from ..appconn.feed_ctrl_connection import FeedCtrlConnection

class Verification:
    def __init__(self):
        self._feedctrl = FeedCtrlConnection
        _hostid = self._feedctrl.get_host_master_id()

    def check_incoming(self, feed_id, is_master=False):
        if is_master:
            return True
        else:
            trusted = set(self._feedctrl.get_trusted(self._hostid))
            blocked = set(self._feedctrl.get_blocked(self._hostid))
            return feed_id in trusted and feed_id not in blocked

    def check_outgoing(self, feed_id):
        master = set(self._feedctrl.get_all_master_ids())
        if (feed_id in master):
            return True
        else:
            trusted = set(self._feedctrl.get_trusted(self._hostid))
            blocked = set(self._feedctrl.get_blocked(self._hostid))
            return feed_id in trusted and feed_id not in blocked

