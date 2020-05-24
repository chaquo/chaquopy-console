import hashlib  # Comes with python
import secrets  # Comes with python
from nacl.signing import SigningKey
from testfixtures import LogCapture
import os
from ..logStore.funcs.event import Content, Event, Meta
from ..logStore.appconn.chat_connection import ChatFunction


def test_get_chat_event():
    try:
        with LogCapture() as log_cap:
            private_key = secrets.token_bytes(32)
            signing_key = SigningKey(private_key)
            public_key_feed_id = signing_key.verify_key.encode()

            content0 = Content('chat/whateveraction',
                               {'messagekey': 'hallo zusammen', 'chat_id': '1', 'timestampkey': 10})
            hash_of_content = hashlib.sha256(content0.get_as_cbor()).hexdigest()
            hash_of_prev = None
            meta = Meta(public_key_feed_id, 0, hash_of_prev, 'ed25519', ('sha256', hash_of_content))
            signature = signing_key.sign(meta.get_as_cbor())._signature
            event = Event(meta, signature, content0).get_as_cbor()

            connector = ChatFunction()
            connector.insert_chat_msg(event)
            meta = Meta(public_key_feed_id, 1, hash_of_prev, 'ed25519', ('sha256', hash_of_content))
            content1 = Content('chat/whateveraction',
                               {'messagekey': 'wie gehts?', 'chat_id': '1', 'timestampkey': 20})
            signature = signing_key.sign(meta.get_as_cbor())._signature
            event = Event(meta, signature, content1).get_as_cbor()
            connector.insert_chat_msg(event)
            content2 = Content('chat/whateveraction',
                               {'messagekey': 'schönes Wetter heute', 'chat_id': '1', 'timestampkey': 30})
            meta = Meta(public_key_feed_id, 2, hash_of_prev, 'ed25519', ('sha256', hash_of_content))
            signature = signing_key.sign(meta.get_as_cbor())._signature
            event = Event(meta, signature, content2).get_as_cbor()
            connector.insert_chat_msg(event)
            print(log_cap)
            q = connector.get_chat_since(15, '1')
            assert q[0][0] == 'wie gehts?'
            assert q[1][0] == 'schönes Wetter heute'
            t = connector.get_full_chat('1')
            assert t[0][0] == 'hallo zusammen'
            assert t[1][0] == 'wie gehts?'
            assert t[2][0] == 'schönes Wetter heute'
        assert True
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
