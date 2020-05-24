import secrets  # Comes with python
from contextlib import contextmanager
import os
from nacl.signing import SigningKey
from ..logStore.funcs.EventCreationTool import EventFactory
from ..logStore.funcs.log import create_logger
from ..logStore.appconn.feed_ctrl_connection import FeedCtrlConnection

logger = create_logger('test_feed_ctrl_connection')


class TestFeedCtrlConnection:

    def test_add_event_and_get_host_master_id(self):
        with session_scope():
            ecf = EventFactory()
            new_event = ecf.next_event('MASTER/MASTER', {})
            fcc = FeedCtrlConnection()
            fcc.add_event(new_event)
            result = fcc.get_host_master_id()
            assert result == ecf.get_feed_id()

    def test_get_trusted(self):
        with session_scope():
            ecf = EventFactory()
            new_event = ecf.next_event('MASTER/MASTER', {})
            fcc = FeedCtrlConnection()
            fcc.add_event(new_event)
            trust_id1 = generate_random_feed_id()
            new_event = ecf.next_event('MASTER/Trust', {'feed_id': trust_id1})
            fcc.add_event(new_event)
            trust_id2 = generate_random_feed_id()
            new_event = ecf.next_event('MASTER/Trust', {'feed_id': trust_id2})
            fcc.add_event(new_event)
            trust_id3 = generate_random_feed_id()
            new_event = ecf.next_event('MASTER/Trust', {'feed_id': trust_id3})
            fcc.add_event(new_event)
            trust_id4 = generate_random_feed_id()
            new_event = ecf.next_event('MASTER/Name', {'name': trust_id4})
            fcc.add_event(new_event)
            trust_id4 = generate_random_feed_id()
            new_event = ecf.next_event('MASTER/NewFeed', {'feed_id': trust_id4, 'app_name': 'TestApp'})
            fcc.add_event(new_event)
            new_event = ecf.next_event('MASTER/Radius', {'radius': 5})
            fcc.add_event(new_event)
            result = fcc.get_trusted(ecf.get_feed_id())
            assert result[0] == trust_id1
            assert result[1] == trust_id2
            assert result[2] == trust_id3
            assert len(result) == 3

    def test_get_blocked(self):
        with session_scope():
            ecf = EventFactory()
            new_event = ecf.next_event('MASTER/MASTER', {})
            fcc = FeedCtrlConnection()
            fcc.add_event(new_event)
            trust_id1 = generate_random_feed_id()
            new_event = ecf.next_event('MASTER/Trust', {'feed_id': trust_id1})
            fcc.add_event(new_event)
            trust_id2 = generate_random_feed_id()
            new_event = ecf.next_event('MASTER/Trust', {'feed_id': trust_id2})
            fcc.add_event(new_event)
            new_event = ecf.next_event('MASTER/Block', {'feed_id': trust_id2})
            fcc.add_event(new_event)
            trust_id3 = generate_random_feed_id()
            new_event = ecf.next_event('MASTER/Trust', {'feed_id': trust_id3})
            fcc.add_event(new_event)
            trust_id4 = generate_random_feed_id()
            new_event = ecf.next_event('MASTER/Block', {'feed_id': trust_id4})
            fcc.add_event(new_event)
            trust_id5 = generate_random_feed_id()
            new_event = ecf.next_event('MASTER/Trust', {'feed_id': trust_id5})
            fcc.add_event(new_event)
            trust_id5 = generate_random_feed_id()
            new_event = ecf.next_event('MASTER/Name', {'name': trust_id5})
            fcc.add_event(new_event)
            trust_id5 = generate_random_feed_id()
            new_event = ecf.next_event('MASTER/NewFeed', {'feed_id': trust_id5, 'app_name': 'TestApp'})
            fcc.add_event(new_event)
            new_event = ecf.next_event('MASTER/Radius', {'radius': 5})
            fcc.add_event(new_event)
            result1 = fcc.get_blocked(ecf.get_feed_id())
            result2 = fcc.get_trusted(ecf.get_feed_id())
            assert result1[0] == trust_id2
            assert result1[1] == trust_id4
            assert result2[0] == trust_id1
            assert result2[1] == trust_id3
            assert len(result1) == 2
            assert len(result2) == 3

    def test_get_all_master_ids(self):
        with session_scope():
            ecf = EventFactory()
            fcc = FeedCtrlConnection()
            new_event = ecf.next_event('MASTER/MASTER', {})
            fcc.add_event(new_event)
            ecf2 = EventFactory()
            new_event1 = ecf2.next_event('MASTER/MASTER', {})
            fcc.add_event(new_event1)
            trust_id2 = generate_random_feed_id()
            new_event = ecf.next_event('MASTER/Trust', {'feed_id': trust_id2})
            fcc.add_event(new_event)
            new_event = ecf.next_event('MASTER/Block', {'feed_id': trust_id2})
            fcc.add_event(new_event)
            fcc.add_event(new_event)
            trust_id5 = generate_random_feed_id()
            new_event = ecf.next_event('MASTER/Trust', {'feed_id': trust_id5})
            fcc.add_event(new_event)
            trust_id5 = generate_random_feed_id()
            new_event = ecf.next_event('MASTER/Name', {'name': trust_id5})
            fcc.add_event(new_event)
            trust_id5 = generate_random_feed_id()
            new_event = ecf.next_event('MASTER/NewFeed', {'feed_id': trust_id5, 'app_name': 'TestApp'})
            fcc.add_event(new_event)
            new_event = ecf.next_event('MASTER/Radius', {'radius': 5})
            fcc.add_event(new_event)
            result1 = fcc.get_all_master_ids()
            assert result1[0] == ecf2.get_feed_id()
            assert len(result1) == 1

    def test_get_all_master_ids_feed_ids(self):
        with session_scope():
            ecf = EventFactory()
            fcc = FeedCtrlConnection()
            new_event = ecf.next_event('MASTER/MASTER', {})
            fcc.add_event(new_event)
            trust_id1 = generate_random_feed_id()
            new_event = ecf.next_event('MASTER/NewFeed', {'feed_id': trust_id1, 'app_name': 'Test1'})
            fcc.add_event(new_event)
            trust_id2 = generate_random_feed_id()
            new_event = ecf.next_event('MASTER/NewFeed', {'feed_id': trust_id2, 'app_name': 'Test2'})
            fcc.add_event(new_event)
            trust_id3 = generate_random_feed_id()
            new_event = ecf.next_event('MASTER/NewFeed', {'feed_id': trust_id3, 'app_name': 'Test3'})
            fcc.add_event(new_event)
            new_event = ecf.next_event('MASTER/Trust', {'feed_id': trust_id3})
            fcc.add_event(new_event)
            trust_id5 = generate_random_feed_id()
            new_event = ecf.next_event('MASTER/Trust', {'feed_id': trust_id5})
            fcc.add_event(new_event)
            trust_id5 = generate_random_feed_id()
            new_event = ecf.next_event('MASTER/Name', {'name': trust_id5})
            fcc.add_event(new_event)
            new_event = ecf.next_event('MASTER/Radius', {'radius': 5})
            fcc.add_event(new_event)
            result = fcc.get_all_master_ids_feed_ids(ecf.get_feed_id())
            assert result[0] == trust_id1
            assert result[1] == trust_id2
            assert result[2] == trust_id3
            assert len(result) == 3

    def test_get_username(self):
        with session_scope():
            ecf = EventFactory()
            fcc = FeedCtrlConnection()
            new_event = ecf.next_event('MASTER/MASTER', {})
            fcc.add_event(new_event)
            new_event = ecf.next_event('MASTER/Name', {'name': 'Alice'})
            fcc.add_event(new_event)
            ecf2 = EventFactory()
            new_event = ecf2.next_event('MASTER/MASTER', {})
            fcc.add_event(new_event)
            new_event = ecf2.next_event('MASTER/Name', {'name': 'Bob'})
            fcc.add_event(new_event)
            trust_id5 = generate_random_feed_id()
            new_event = ecf.next_event('MASTER/Trust', {'feed_id': trust_id5})
            fcc.add_event(new_event)
            trust_id5 = generate_random_feed_id()
            new_event = ecf.next_event('MASTER/NewFeed', {'feed_id': trust_id5, 'app_name': 'TestApp'})
            fcc.add_event(new_event)
            new_event = ecf.next_event('MASTER/Radius', {'radius': 5})
            fcc.add_event(new_event)
            new_event = ecf.next_event('MASTER/Name', {'name': 'Patrice'})
            fcc.add_event(new_event)
            result1 = fcc.get_username(ecf.get_feed_id())
            result2 = fcc.get_username(ecf2.get_feed_id())
            assert result1 == 'Patrice'
            assert result2 == 'Bob'

    def test_get_my_last_event(self):
        with session_scope():
            ecf = EventFactory()
            fcc = FeedCtrlConnection()
            new_event = ecf.next_event('MASTER/MASTER', {})
            fcc.add_event(new_event)
            trust_id5 = generate_random_feed_id()
            new_event = ecf.next_event('MASTER/Trust', {'feed_id': trust_id5})
            fcc.add_event(new_event)
            trust_id5 = generate_random_feed_id()
            new_event = ecf.next_event('MASTER/NewFeed', {'feed_id': trust_id5, 'app_name': 'TestApp'})
            fcc.add_event(new_event)
            new_event = ecf.next_event('MASTER/Radius', {'radius': 5})
            fcc.add_event(new_event)
            new_event = ecf.next_event('MASTER/Name', {'name': 'Patrice'})
            fcc.add_event(new_event)
            last_event = ecf.next_event('MASTER/Name', {'name': 'Alice'})
            fcc.add_event(last_event)
            ecf2 = EventFactory()
            new_event = ecf2.next_event('MASTER/MASTER', {})
            fcc.add_event(new_event)
            new_event = ecf2.next_event('MASTER/Name', {'name': 'Bob'})
            fcc.add_event(new_event)
            result = fcc.get_my_last_event()
            assert result == last_event

    def test_get_radius(self):
        with session_scope():
            ecf = EventFactory()
            fcc = FeedCtrlConnection()
            new_event = ecf.next_event('MASTER/MASTER', {})
            fcc.add_event(new_event)
            last_event = ecf.next_event('MASTER/Radius', {'radius': 5})
            fcc.add_event(last_event)
            ecf2 = EventFactory()
            new_event = ecf2.next_event('MASTER/MASTER', {})
            fcc.add_event(new_event)
            new_event = ecf2.next_event('MASTER/Radius', {'radius': 3})
            fcc.add_event(new_event)
            new_event = ecf2.next_event('MASTER/Name', {'name': 'Alice'})
            fcc.add_event(new_event)
            trust_id5 = generate_random_feed_id()
            new_event = ecf.next_event('MASTER/Trust', {'feed_id': trust_id5})
            fcc.add_event(new_event)
            trust_id5 = generate_random_feed_id()
            new_event = ecf.next_event('MASTER/NewFeed', {'feed_id': trust_id5, 'app_name': 'TestApp'})
            fcc.add_event(new_event)
            new_event = ecf.next_event('MASTER/Radius', {'radius': 5})
            fcc.add_event(new_event)
            new_event = ecf.next_event('MASTER/Name', {'name': 'Patrice'})
            fcc.add_event(new_event)
            result = fcc.get_radius()
            assert result == 5

    def test_get_master_id_from_feed(self):
        with session_scope():
            ecf = EventFactory()
            fcc = FeedCtrlConnection()
            new_event = ecf.next_event('MASTER/MASTER', {})
            fcc.add_event(new_event)
            trust_id1 = generate_random_feed_id()
            new_event = ecf.next_event('MASTER/NewFeed', {'feed_id': trust_id1, 'app_name': 'Test1'})
            fcc.add_event(new_event)
            ecf2 = EventFactory()
            new_event = ecf2.next_event('MASTER/MASTER', {})
            fcc.add_event(new_event)
            trust_id2 = generate_random_feed_id()
            new_event = ecf2.next_event('MASTER/NewFeed', {'feed_id': trust_id2, 'app_name': 'Test2'})
            fcc.add_event(new_event)
            new_event = ecf2.next_event('MASTER/Name', {'name': 'Alice'})
            fcc.add_event(new_event)
            trust_id5 = generate_random_feed_id()
            new_event = ecf.next_event('MASTER/Trust', {'feed_id': trust_id5})
            fcc.add_event(new_event)
            trust_id5 = generate_random_feed_id()
            new_event = ecf.next_event('MASTER/NewFeed', {'feed_id': trust_id5, 'app_name': 'TestApp'})
            fcc.add_event(new_event)
            new_event = ecf.next_event('MASTER/Radius', {'radius': 5})
            fcc.add_event(new_event)
            new_event = ecf.next_event('MASTER/Name', {'name': 'Patrice'})
            fcc.add_event(new_event)
            result1 = fcc.get_master_id_from_feed(trust_id1)
            result2 = fcc.get_master_id_from_feed(trust_id2)
            assert result1 == ecf.get_feed_id()
            assert result2 == ecf2.get_feed_id()

    def test_get_application_name(self):
        with session_scope():
            ecf = EventFactory()
            fcc = FeedCtrlConnection()
            new_event = ecf.next_event('MASTER/MASTER', {})
            fcc.add_event(new_event)
            trust_id1 = generate_random_feed_id()
            new_event = ecf.next_event('MASTER/NewFeed', {'feed_id': trust_id1, 'app_name': 'Test1'})
            fcc.add_event(new_event)
            ecf2 = EventFactory()
            new_event = ecf2.next_event('MASTER/MASTER', {})
            fcc.add_event(new_event)
            trust_id2 = generate_random_feed_id()
            new_event = ecf2.next_event('MASTER/NewFeed', {'feed_id': trust_id2, 'app_name': 'Test2'})
            fcc.add_event(new_event)
            new_event = ecf2.next_event('MASTER/Name', {'name': 'Alice'})
            fcc.add_event(new_event)
            trust_id5 = generate_random_feed_id()
            new_event = ecf.next_event('MASTER/Trust', {'feed_id': trust_id5})
            fcc.add_event(new_event)
            trust_id5 = generate_random_feed_id()
            new_event = ecf.next_event('MASTER/NewFeed', {'feed_id': trust_id5, 'app_name': 'TestApp'})
            fcc.add_event(new_event)
            new_event = ecf.next_event('MASTER/Radius', {'radius': 5})
            fcc.add_event(new_event)
            new_event = ecf.next_event('MASTER/Name', {'name': 'Patrice'})
            fcc.add_event(new_event)
            result1 = fcc.get_application_name(trust_id1)
            result2 = fcc.get_application_name(trust_id2)
            logger.error(result1)
            assert result1 == 'Test1'
            assert result2 == 'Test2'

    def test_get_feed_ids_from_application_in_master_id(self):
        with session_scope():
            ecf = EventFactory()
            fcc = FeedCtrlConnection()
            new_event = ecf.next_event('MASTER/MASTER', {})
            fcc.add_event(new_event)
            trust_id1 = generate_random_feed_id()
            new_event = ecf.next_event('MASTER/NewFeed', {'feed_id': trust_id1, 'app_name': 'Test1'})
            fcc.add_event(new_event)
            trust_id3 = generate_random_feed_id()
            new_event = ecf.next_event('MASTER/NewFeed', {'feed_id': trust_id3, 'app_name': 'Test1'})
            fcc.add_event(new_event)
            ecf2 = EventFactory()
            new_event = ecf2.next_event('MASTER/MASTER', {})
            fcc.add_event(new_event)
            trust_id2 = generate_random_feed_id()
            new_event = ecf2.next_event('MASTER/NewFeed', {'feed_id': trust_id2, 'app_name': 'Test2'})
            fcc.add_event(new_event)
            new_event = ecf2.next_event('MASTER/Name', {'name': 'Alice'})
            fcc.add_event(new_event)
            trust_id5 = generate_random_feed_id()
            new_event = ecf.next_event('MASTER/Trust', {'feed_id': trust_id5})
            fcc.add_event(new_event)
            trust_id5 = generate_random_feed_id()
            new_event = ecf.next_event('MASTER/NewFeed', {'feed_id': trust_id5, 'app_name': 'TestApp'})
            fcc.add_event(new_event)
            new_event = ecf.next_event('MASTER/Radius', {'radius': 5})
            fcc.add_event(new_event)
            new_event = ecf.next_event('MASTER/Name', {'name': 'Patrice'})
            fcc.add_event(new_event)
            result1 = fcc.get_feed_ids_from_application_in_master_id(ecf.get_feed_id(), 'Test1')
            result2 = fcc.get_feed_ids_from_application_in_master_id(ecf2.get_feed_id(), 'Test2')
            logger.error(result1)
            assert result1[0] == trust_id1
            assert result2[0] == trust_id2
            assert result1[1] == trust_id3

    def test_get_feed_ids_in_radius(self):
        with session_scope():
            ecf = EventFactory()
            fcc = FeedCtrlConnection()
            new_event = ecf.next_event('MASTER/MASTER', {})
            fcc.add_event(new_event)
            new_event = ecf.next_event('MASTER/Radius', {'radius': 3})
            fcc.add_event(new_event)
            ecf2 = EventFactory()
            new_event = ecf2.next_event('MASTER/MASTER', {})
            fcc.add_event(new_event)
            new_event = ecf2.next_event('MASTER/Radius', {'radius': 5})
            fcc.add_event(new_event)
            ecf3 = EventFactory()
            new_event = ecf3.next_event('MASTER/MASTER', {})
            fcc.add_event(new_event)
            new_event = ecf3.next_event('MASTER/Radius', {'radius': 1})
            fcc.add_event(new_event)
            ecf4 = EventFactory()
            new_event = ecf4.next_event('MASTER/MASTER', {})
            fcc.add_event(new_event)
            new_event = ecf4.next_event('MASTER/Radius', {'radius': 2})
            fcc.add_event(new_event)
            new_event = ecf4.next_event('MASTER/Name', {'name': 'Alice'})
            fcc.add_event(new_event)
            new_event = ecf2.next_event('MASTER/Name', {'name': 'Alice'})
            fcc.add_event(new_event)
            trust_id5 = generate_random_feed_id()
            new_event = ecf.next_event('MASTER/Trust', {'feed_id': trust_id5})
            fcc.add_event(new_event)
            trust_id5 = generate_random_feed_id()
            new_event = ecf.next_event('MASTER/NewFeed', {'feed_id': trust_id5, 'app_name': 'TestApp'})
            fcc.add_event(new_event)
            new_event = ecf.next_event('MASTER/Radius', {'radius': 5})
            fcc.add_event(new_event)
            new_event = ecf.next_event('MASTER/Name', {'name': 'Patrice'})
            fcc.add_event(new_event)
            result = fcc.get_feed_ids_in_radius()
            assert result[0] == ecf.get_feed_id()
            assert result[1] == ecf3.get_feed_id()
            assert result[2] == ecf4.get_feed_id()
            assert len(result) == 3

    def test_set_radius(self):
        with session_scope():
            ecf = EventFactory()
            fcc = FeedCtrlConnection()
            new_event = ecf.next_event('MASTER/MASTER', {})
            fcc.add_event(new_event)
            last_event = ecf.next_event('MASTER/Radius', {'radius': 5})
            fcc.add_event(last_event)
            ecf2 = EventFactory()
            new_event = ecf2.next_event('MASTER/MASTER', {})
            fcc.add_event(new_event)
            new_event = ecf2.next_event('MASTER/Radius', {'radius': 3})
            fcc.add_event(new_event)
            new_event = ecf2.next_event('MASTER/Name', {'name': 'Alice'})
            fcc.add_event(new_event)
            new_event = ecf2.next_event('MASTER/Name', {'name': 'Alice'})
            fcc.add_event(new_event)
            trust_id5 = generate_random_feed_id()
            new_event = ecf.next_event('MASTER/Trust', {'feed_id': trust_id5})
            fcc.add_event(new_event)
            trust_id5 = generate_random_feed_id()
            new_event = ecf.next_event('MASTER/NewFeed', {'feed_id': trust_id5, 'app_name': 'TestApp'})
            fcc.add_event(new_event)
            new_event = ecf.next_event('MASTER/Radius', {'radius': 5})
            fcc.add_event(new_event)
            new_event = ecf.next_event('MASTER/Name', {'name': 'Patrice'})
            fcc.add_event(new_event)
            fcc.set_feed_ids_radius(ecf.get_feed_id(), 6)
            fcc.set_feed_ids_radius(ecf2.get_feed_id(), 10)
            result = fcc.get_radius()
            assert result == 6


def generate_random_feed_id():
    private_key = secrets.token_bytes(32)
    signing_key = SigningKey(private_key)
    public_key_feed_id = signing_key.verify_key.encode()
    return public_key_feed_id


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    try:
        yield
    except Exception as e:
        logger.error(e)
        raise
    finally:
        try:
            if os.path.exists('cborDatabase.sqlite'):
                os.remove('cborDatabase.sqlite')
                if os.path.exists('eventDatabase.sqlite'):
                    os.remove('eventDatabase.sqlite')
                    directory = "./"
                    files_in_directory = os.listdir(directory)
                    filtered_files = [file for file in files_in_directory if file.endswith(".key")]
                    for file in filtered_files:
                        path_to_file = os.path.join(directory, file)
                        os.remove(path_to_file)
            else:
                assert False
        except Exception as e:
            logger.error(e)
