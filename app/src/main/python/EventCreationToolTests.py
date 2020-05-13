import hashlib
import nacl.signing
import nacl.encoding
import nacl.exceptions
import EventCreationTool
import Event
from com.chaquo.python import Python

# LOOK AT THE README THIS FILE IS GOING TO BE THE TESTFILE LATER ON

FILES_DIR = str(Python.getPlatform().getApplication().getFilesDir())

def verify_event(event, previous_event=None):
    if previous_event is not None:
        previous_hash_type, hash_of_previous = event.meta.hash_of_prev
        prev_meta_as_cbor = previous_event.meta.get_as_cbor()
        if previous_event.meta.feed_id != event.meta.feed_id:
            return False
        if event.meta.seq_no - 1 != previous_event.meta.seq_no:
            return False
        if not (previous_hash_type == 0 and hashlib.sha256(prev_meta_as_cbor).digest() == hash_of_previous):
            return False

    content_hash_type, hash_of_content = event.meta.hash_of_content
    signature_identifier = event.meta.signature_info
    signature = event.signature

    content = event.content.get_as_cbor()
    meta_as_cbor = event.meta.get_as_cbor()

    if not (content_hash_type == 0 and hashlib.sha256(content).digest() == hash_of_content):
        return False

    if signature_identifier == 0:
        verification_key = nacl.signing.VerifyKey(event.meta.feed_id)
        try:
            verification_key.verify(meta_as_cbor, signature)
        except nacl.exceptions.BadSignatureError:
            return False
    #elif signature_identifier == 1:
    #    secret_key = DB.get_secret_hmac_key(event.meta.feed_id)
    #    if secret_key is None:
    #        return False
    #    generated_signature = hmac.new(secret_key, meta_as_cbor, hashlib.sha256).hexdigest()
    #    if signature != generated_signature:
    #        return False
    else:
        return False

    return True


def main():
    eg = EventCreationTool.EventFactory(path_to_keys=str(Python.getPlatform().getApplication().getFilesDir()), path_to_keys_relative=False)
    first_event = eg.next_event('whateverapp/whateveraction', {'somekey': 'somevalue', 'someotherkey': 4932})
    second_event = eg.next_event('whateverapp/whateveraction', {'okkey': 'xd', 382473287: 2389748293, 432787: 44})
    third_event = eg.next_event('whateverapp/whateveraction', {'somekey': 'somevalue', 'someotherkey': 4932})
    first_event_object = Event.Event.from_cbor(first_event)
    print(first_event_object.meta.seq_no)
    second_event_object = Event.Event.from_cbor(second_event)
    print(second_event_object.meta.seq_no)
    third_event_object = Event.Event.from_cbor(third_event)
    print(third_event_object.meta.seq_no)
    egt = EventCreationTool.EventFactory(path_to_keys=FILES_DIR, path_to_keys_relative=False, last_event=third_event)
    fourth_event = egt.next_event('whateverapp/whateveraction', {'somekey': 'somevalue', 'someotherkey': 4932})
    fourth_event_object = Event.Event.from_cbor(fourth_event)
    print(fourth_event_object.meta.seq_no)
