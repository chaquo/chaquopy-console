from ECT_FCTRL_DB.logStore.appconn.feed_ctrl_connection import FeedCtrlConnection
from ECT_FCTRL_DB.logStore.funcs.log import create_logger

logger = create_logger('Radius')


class Radius:

    def __init__(self):
        self._fcc = FeedCtrlConnection()
        self._hostID = self._fcc.get_host_master_id()

    def calculate_radius(self):
        radius = self._fcc.get_radius()
        self.__check_trusted(self._hostID, radius, 'MASTER')

    def __check_trusted(self, master_id, radius, prev_app_name, step=1, ):
        if radius and step is not None:
            if radius < 1 or step > radius:
                return
            trusted = self._fcc.get_trusted(master_id)
            if not len(trusted) == 0:
                for trusted_id in trusted:
                    application_name = self._fcc.get_application_name(trusted_id)
                    master = None
                    if application_name == 'MASTER':
                        master = trusted_id
                        if master != self._hostID:
                            self._fcc.set_feed_ids_radius(master, step)
                    elif application_name == prev_app_name or prev_app_name == 'MASTER':
                        master = self._fcc.get_master_id_from_feed(trusted_id)
                        if master != self._hostID:
                            self._fcc.set_feed_ids_radius(master, step)
                    else:
                        return
                    self.__check_trusted(master, radius, application_name, step + 1)
            else:
                return
