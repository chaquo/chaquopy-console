import secrets  # Comes with python
from contextlib import contextmanager
import os
from nacl.signing import SigningKey
from logStore.funcs.log import create_logger
from logStore.verific.verify_insertion import Verification
from logStore.funcs.EventCreationTool import EventFactory
from logStore.appconn.feed_ctrl_connection import FeedCtrlConnection

logger = create_logger('test_verify_insertion')


class TestVerification:
    """Tests if incoming master_ids is accepted"""

    def test_incoming_master(self):
        with session_scope():
            master_id = generate_random_feed_id()
            ver = Verification()
            result = ver.check_incoming(master_id, 'MASTER')
            assert result is True

    """Tests if incoming trusted feed_id is accepted"""

    def test_incoming_trusted(self):
        with session_scope():
            ver = Verification()
            ecf = EventFactory()
            new_event = ecf.next_event('MASTER/MASTER', {})
            fcc = FeedCtrlConnection()
            fcc.add_event(new_event)
            trust_id1 = generate_random_feed_id()
            new_event = ecf.next_event('MASTER/Trust', {'feed_id': trust_id1})
            fcc.add_event(new_event)
            assert ver.check_incoming(trust_id1, 'TestApp1') is True

    """Tests if incoming not trusted is discarded"""

    def test_incoming_not_trusted(self):
        with session_scope():
            ecf = EventFactory()
            ver = Verification()
            new_event = ecf.next_event('MASTER/MASTER', {})
            fcc = FeedCtrlConnection()
            fcc.add_event(new_event)
            trust_id1 = generate_random_feed_id()
            assert ver.check_incoming(trust_id1, 'TestApp1') is False

    """Tests if incoming blocked are discarded"""

    def test_incoming_blocked(self):
        with session_scope():
            ecf = EventFactory()
            ver = Verification()
            new_event = ecf.next_event('MASTER/MASTER', {})
            fcc = FeedCtrlConnection()
            fcc.add_event(new_event)
            trust_id1 = generate_random_feed_id()
            new_event = ecf.next_event('MASTER/Block', {'feed_id': trust_id1})
            fcc.add_event(new_event)
            assert ver.check_incoming(trust_id1, 'TestApp1') is False

    """Tests if outgoing master is accepted"""

    def test_outgoing_master(self):
        with session_scope():
            fcc = FeedCtrlConnection()
            ecf = EventFactory()
            new_event = ecf.next_event('MASTER/MASTER', {})
            fcc.add_event(new_event)
            ver = Verification()
            result = ver.check_outgoing(ecf.get_feed_id())
            assert result is True

    """Tests if outgoing trusted is accepted"""

    def test_outgoing_trusted(self):
        with session_scope():
            fcc = FeedCtrlConnection()
            ecf = EventFactory()
            new_event = ecf.next_event('MASTER/MASTER', {})
            fcc.add_event(new_event)
            trust_id1 = generate_random_feed_id()
            new_event = ecf.next_event('MASTER/Trust', {'feed_id': trust_id1})
            fcc.add_event(new_event)
            ver = Verification()
            result = ver.check_outgoing(trust_id1)
            assert result is True

    """Tests if outgoing not trusted is discarded"""

    def test_outgoing_not_trusted(self):
        with session_scope():
            fcc = FeedCtrlConnection()
            ecf = EventFactory()
            new_event = ecf.next_event('MASTER/MASTER', {})
            fcc.add_event(new_event)
            trust_id1 = generate_random_feed_id()
            ver = Verification()
            result = ver.check_outgoing(trust_id1)
            assert result is False

    """Tests if outgoing blocked is discarded"""

    def test_outgoing_blocked(self):
        with session_scope():
            fcc = FeedCtrlConnection()
            ecf = EventFactory()
            new_event = ecf.next_event('MASTER/MASTER', {})
            fcc.add_event(new_event)
            trust_id1 = generate_random_feed_id()
            new_event = ecf.next_event('MASTER/Block', {'feed_id': trust_id1})
            fcc.add_event(new_event)
            ver = Verification()
            result = ver.check_outgoing(trust_id1)
            assert result is False

    """Tests if feed_id is inside the given radius"""

    def test_in_radius(self):
        with session_scope():
            ver = Verification()
            fcc = FeedCtrlConnection()
            ecf1 = EventFactory()
            new_event = ecf1.next_event('MASTER/MASTER', {})
            fcc.add_event(new_event)
            last_event = ecf1.next_event('MASTER/Radius', {'radius': 5})
            fcc.add_event(last_event)
            ecf2 = EventFactory()
            new_event = ecf2.next_event('MASTER/MASTER', {})
            fcc.add_event(new_event)
            last_event = ecf2.next_event('MASTER/Radius', {'radius': 3})
            fcc.add_event(last_event)
            ecf3 = EventFactory()
            new_event = ecf3.next_event('MASTER/MASTER', {})
            fcc.add_event(new_event)
            new_event = ecf3.next_event('MASTER/Radius', {'radius': 3})
            fcc.add_event(new_event)
            trusted_id1 = generate_random_feed_id()
            new_event = ecf3.next_event('MASTER/NewFeed', {'feed_id': trusted_id1, 'app_name': 'TestApp'})
            fcc.add_event(new_event)
            trusted_id2 = generate_random_feed_id()
            new_event = ecf2.next_event('MASTER/NewFeed', {'feed_id': trusted_id2, 'app_name': 'TestApp'})
            fcc.add_event(new_event)
            new_event = ecf1.next_event('MASTER/Trust', {'feed_id': trusted_id2})
            fcc.add_event(new_event)
            new_event = ecf2.next_event('MASTER/Trust', {'feed_id': trusted_id1})
            fcc.add_event(new_event)
            result = ver._check_in_radius('TestApp')
            assert result


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
