# Tests for EventCreationTool.py
# Authors: Günes Aydin, Joey Zgraggen, Nikodem Kernbach
# VERSION: 1.1

# Since only the EventFactory class is our recommended API, it is the only one tested.

import hashlib
import hmac
import nacl.signing
import os
import secrets
import shutil
import unittest
import Event
import EventCreationTool

TEST_FOLDER_RELATIVE_PATH = 'tmp_test_folder'  # Path for temporarily stored folder (used to keep testing key files)


class EventFactoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):  # Creates folder for testing key files
        if not os.path.exists(TEST_FOLDER_RELATIVE_PATH):
            os.mkdir(TEST_FOLDER_RELATIVE_PATH)

    # Tests whether the hashing algorithms are enforced correctly
    def test_constructor_hashing_algorithms(self):
        ef = EventCreationTool.EventFactory(path_to_keys=TEST_FOLDER_RELATIVE_PATH)
        ef.first_event('whateverapp', secrets.token_bytes(32))
        event = ef.next_event('whateverapp/whateveraction', {'somekey': 438927432})
        event = Event.Event.from_cbor(event)
        # By default SHA256 hashing algorithm should be used
        self.assertEqual(event.meta.hash_of_content[0], EventCreationTool.EventCreationTool._HASH_INFO['sha256'],
                          "The tool uses the wrong hashing algorithm by default")
        # Check if hash is calculated correctly
        self.assertEqual(event.meta.hash_of_content[1], hashlib.sha256(event.content.get_as_cbor()).digest(),
                          "Hash is not the SHA256 hash of the event content")
        # Check if using a wrong hashing algorithm throws an exception
        self.assertRaises(EventCreationTool.HashingAlgorithmNotFoundException,
                          EventCreationTool.EventFactory, path_to_keys=TEST_FOLDER_RELATIVE_PATH,
                          hashing_algorithm='thisisnotahashingalgorithm')

    # Tests whether the signing algorithms are enforced correctly
    def test_constructor_signing_algorithms(self):
        ef = EventCreationTool.EventFactory(path_to_keys=TEST_FOLDER_RELATIVE_PATH)
        ef.first_event('whateverapp', secrets.token_bytes(32))
        event = ef.next_event('whateverapp/whateveraction', {'somekey': 438927432})
        event = Event.Event.from_cbor(event)
        # By default ED25519 signing algorithm should be used
        self.assertEqual(event.meta.signature_info, EventCreationTool.EventCreationTool._SIGN_INFO['ed25519'],
                         "The tool uses the wrong signing algorithm by default")
        signKey = nacl.signing.SigningKey(ef.get_private_key())
        # Check if signature is calculated correctly
        self.assertEqual(event.signature, signKey.sign(event.meta.get_as_cbor()).signature,
                         "Signature is not the correct ED25519 signature of the meta cbor bytes")
        ef2 = EventCreationTool.EventFactory(path_to_keys=TEST_FOLDER_RELATIVE_PATH, signing_algorithm='hmac_sha256')
        ef2.first_event('whateverapp', secrets.token_bytes(32))
        event2 = ef2.next_event('someapp/somevalue', {'skey': 12312})
        event2 = Event.Event.from_cbor(event2)
        # Check if signature type is hmac_sha256
        self.assertEqual(event2.meta.signature_info, EventCreationTool.EventCreationTool._SIGN_INFO['hmac_sha256'],
                         "The wrong signing algorithm is indicated inside the event")
        # Check if hmac_sha256 signature was calculated correctly
        self.assertEqual(event2.signature,
                         hmac.new(ef2.get_private_key(), event2.meta.get_as_cbor(), hashlib.sha256).digest(),
                         "Signature is not the correct HMAC_SHA256 signature of the meta cbor bytes")
        # Check if using an unsupported signing algorithm throws an error.
        self.assertRaises(EventCreationTool.SigningAlgorithmNotFoundException,
                          EventCreationTool.EventFactory, path_to_keys=TEST_FOLDER_RELATIVE_PATH,
                          signing_algorithm='thisisnotasigningalgorithm')

    # Tests whether the initialization of EventFactory objects using an event works correctly
    def test_constructor_with_last_event(self):
        ef = EventCreationTool.EventFactory(path_to_keys=TEST_FOLDER_RELATIVE_PATH, signing_algorithm='hmac_sha256')
        ef.first_event('whateverapp', secrets.token_bytes(32))
        event = ef.next_event('whateverapp/somecommand', {8739: 783, 'otherkey': 'hfe'})
        ef2 = EventCreationTool.EventFactory(last_event=event, path_to_keys=TEST_FOLDER_RELATIVE_PATH,
                                             signing_algorithm='hmac_sha256')
        event2 = ef2.next_event('whateverapp/somecommand', {89342: 'okok'})
        event = Event.Event.from_cbor(event)
        event2 = Event.Event.from_cbor(event2)
        # Check whether the event is a valid continuation of the feed
        self.assertEqual(event.meta.feed_id, event2.meta.feed_id, "The feed ids do not match")
        self.assertEqual(event.meta.seq_no + 1, event2.meta.seq_no, "The sequence number is not continued correctly")
        self.assertEqual(event.meta.signature_info, event2.meta.signature_info, "The signature types do not match")
        self.assertEqual(hashlib.sha256(event.meta.get_as_cbor()).digest(), event2.meta.hash_of_prev[1],
                         "The hash chain is broken")
        # Check the EventFactory objects itself
        self.assertEqual(ef.get_private_key(), ef2.get_private_key(), "The feed ids do not match")
        self.assertEqual(ef.get_feed_id(), ef.get_feed_id(), "Different private keys are used for the same feed")

    def test_next_event_first_event(self):
        ef = EventCreationTool.EventFactory(path_to_keys=TEST_FOLDER_RELATIVE_PATH)
        event = ef.first_event('whateverapp', secrets.token_bytes(32))
        event = Event.Event.from_cbor(event)
        # Check if first event has correct sequence number and matches the objects feed id
        self.assertEqual(event.meta.feed_id, ef.get_feed_id(), "Event contains wrong feed id")
        self.assertEqual(event.meta.seq_no, 0, "The first created event has not sequence number 0")

    def test_next_event_correct_chaining(self):
        ef = EventCreationTool.EventFactory(path_to_keys=TEST_FOLDER_RELATIVE_PATH)
        ef.first_event('whateverapp', secrets.token_bytes(32))
        event = ef.next_event('whateverapp/somecommand', {8739: 783, 'otherkey': 'hfe'})
        event2 = ef.next_event('whateverapp/somecommand', {89342: 'okok'})
        event = Event.Event.from_cbor(event)
        event2 = Event.Event.from_cbor(event2)
        # Check whether the event is a valid continuation of the feed
        self.assertEqual(event.meta.feed_id, event2.meta.feed_id, "The feed ids do not match")
        self.assertEqual(event.meta.seq_no + 1, event2.meta.seq_no, "The sequence number is not continued correctly")
        self.assertEqual(event.meta.signature_info, event2.meta.signature_info, "The signature types do not match")
        self.assertEqual(hashlib.sha256(event.meta.get_as_cbor()).digest(), event2.meta.hash_of_prev[1],
                         "The hash chain is broken")

    def test_factory_enforces_correct_usage_of_of_first_event(self):
        ef = EventCreationTool.EventFactory(path_to_keys=TEST_FOLDER_RELATIVE_PATH)
        self.assertRaises(EventCreationTool.FirstEventWasNotCreatedException,
                          ef.next_event, 'whateverapp/somecommand', {8739: 783, 'otherkey': 'hfe'})
        ef2 = EventCreationTool.EventFactory(path_to_keys=TEST_FOLDER_RELATIVE_PATH)
        ef2.first_event('whateverapp', secrets.token_bytes(32))
        self.assertRaises(EventCreationTool.FirstEventWasAlreadyCreatedException,
                          ef2.first_event, 'whateverapp', secrets.token_bytes(32))

    @classmethod
    def tearDownClass(cls):  # Deletes folder used to keep testing key files
        shutil.rmtree(TEST_FOLDER_RELATIVE_PATH)


if __name__ == '__main__':
    # Run all tests from inside this file
    unittest.main()
