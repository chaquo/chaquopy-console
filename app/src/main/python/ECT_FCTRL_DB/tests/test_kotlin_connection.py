import hashlib  # Comes with python
import secrets  # Comes with python
from nacl.signing import SigningKey
from testfixtures import LogCapture
import os
from ..logStore.funcs.event import Content, Event, Meta
from ..logStore.appconn.kotlin_connection import KotlinFunction


def test_get_kotlin_event():
    try:
        with LogCapture() as log_cap:
            private_key = secrets.token_bytes(32)
            signing_key = SigningKey(private_key)
            public_key_feed_id = signing_key.verify_key.encode()

            private_key2 = secrets.token_bytes(32)
            signing_key2 = SigningKey(private_key2)
            public_key_feed_id2 = signing_key2.verify_key.encode()

            private_key3 = secrets.token_bytes(32)
            signing_key3 = SigningKey(private_key3)
            public_key_feed_id3 = signing_key3.verify_key.encode()

            content00 = Content('KotlinUI/username',
                                {'newUsername': 'Bob', 'oldUsername': '',
                                 'timestamp': 1})
            hash_of_content = hashlib.sha256(content00.get_as_cbor()).hexdigest()
            hash_of_prev = None
            meta = Meta(public_key_feed_id, 0, hash_of_prev, 'ed25519', ('sha256', hash_of_content))
            signature = signing_key.sign(meta.get_as_cbor())._signature
            event = Event(meta, signature, content00).get_as_cbor()

            connector = KotlinFunction()
            connector.insert_data(event)

            meta = Meta(public_key_feed_id2, 0, hash_of_prev, 'ed25519', ('sha256', hash_of_content))
            content01 = Content('KotlinUI/username',
                                {'newUsername': 'Alice', 'oldUsername': '', 'timestamp': 2})
            signature = signing_key.sign(meta.get_as_cbor())._signature
            event = Event(meta, signature, content01).get_as_cbor()
            connector.insert_data(event)

            meta = Meta(public_key_feed_id3, 0, hash_of_prev, 'ed25519', ('sha256', hash_of_content))
            content02 = Content('KotlinUI/username',
                                {'newUsername': 'Max', 'oldUsername': '', 'timestamp': 3})
            signature = signing_key.sign(meta.get_as_cbor())._signature
            event = Event(meta, signature, content02).get_as_cbor()
            connector.insert_data(event)

            meta = Meta(public_key_feed_id, 1, hash_of_prev, 'ed25519', ('sha256', hash_of_content))
            content = Content('KotlinUI/post',
                              {'text': 'Hi Alice, nice to hear from you', 'username': 'Bob',
                               'timestamp': 11})
            signature = signing_key.sign(meta.get_as_cbor())._signature
            event = Event(meta, signature, content).get_as_cbor()
            connector.insert_data(event)

            meta = Meta(public_key_feed_id2, 1, hash_of_prev, 'ed25519', ('sha256', hash_of_content))
            content1 = Content('KotlinUI/post',
                               {'text': 'Hi Bob', 'username': 'Alice', 'timestamp': 15})
            signature = signing_key.sign(meta.get_as_cbor())._signature
            event = Event(meta, signature, content1).get_as_cbor()
            connector.insert_data(event)

            content2 = Content('KotlinUI/post',
                               {'text': 'Hello everyone', 'username': 'Max',
                                'timestamp': 17})
            meta = Meta(public_key_feed_id3, 1, hash_of_prev, 'ed25519', ('sha256', hash_of_content))
            signature = signing_key.sign(meta.get_as_cbor())._signature
            event = Event(meta, signature, content2).get_as_cbor()
            connector.insert_data(event)

            meta = Meta(public_key_feed_id2, 2, hash_of_prev, 'ed25519', ('sha256', hash_of_content))
            content01 = Content('KotlinUI/username',
                                {'newUsername': 'Alice2', 'oldUsername': 'Alice', 'timestamp': 20})
            signature = signing_key.sign(meta.get_as_cbor())._signature
            event = Event(meta, signature, content01).get_as_cbor()
            connector.insert_data(event)

            s = connector.get_all_kotlin_events()
            assert s[0][0] == 'username'
            assert s[1][0] == 'username'
            assert s[3][0] == 'post'
            p = connector.get_usernames_and_feed_id()
            assert p[0][0] == 'Bob'
            assert p[1][0] == 'Alice2'
            q = connector.get_all_entries_by_feed_id(public_key_feed_id)
            assert q[0][3] == 1
            assert q[1][2] == 11
            m = connector.get_last_kotlin_event()
            t = Event.from_cbor(m)
            assert t.content.content[0] == 'KotlinUI/username'
            assert True
            print(log_cap)

    finally:
        try:
            if os.path.exists('cborDatabase.sqlite'):
                os.remove('cborDatabase.sqlite')
                if os.path.exists('eventDatabase.sqlite'):
                    os.remove('eventDatabase.sqlite')
            else:
                assert False
        except PermissionError:
            print('Database is still in use')
