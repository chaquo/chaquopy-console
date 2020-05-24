# This is a wrapper for simple BACnet event handling provided by group 4 logMerge
# Authors: Günes Aydin, Joey Zgraggen, Nikodem Kernbach
# VERSION: 1.5

# For documentation how to use this tool, please refer to README.md

import ECT_FCTRL_DB.eventCreationTool.Event as Event# Our representation of an feed event, please refer to Event.py
import hashlib
import hmac
import secrets
import nacl.signing  # install with 'pip install pynacl'
import nacl.encoding
import os

# !!! For the code to work your also need to install cbor2 (This is used inside Event.py) !!!
# Install with: 'pip install cbor2'


class HashingAlgorithmNotFoundException(Exception):
    def __init__(self):
        super().__init__("The hashing algorithm you specified is unknown to this version of the EventCreationTool")


class SigningAlgorithmNotFoundException(Exception):
    def __init__(self):
        super().__init__("The signing algorithm you specified is unknown to this version of the EventCreationTool")


class KeyFileNotFoundException(Exception):
    def __init__(self):
        super().__init__("Sorry, it seems that you are not the owner of the specified feed. "
                         + "The private key was not found at the specified path.")


class IllegalArgumentTypeException(Exception):
    def __init__(self, list_of_supported_types):
        if not list_of_supported_types or not isinstance(list_of_supported_types, set):
            super().__init__("You called the method with an argument of wrong type!")
        else:
            super().__init__("You called the method with an argument of wrong type! Supported types are:"
                             + ' '.join(list_of_supported_types))


class EventCreationTool:

    # These are the currently supported signing/hashing algorithms. Contact us if you need another one!
    _SIGN_INFO = {'ed25519': 0, 'hmac_sha256': 1}
    _HASH_INFO = {'sha256': 0}

    @classmethod
    def get_stored_feed_ids(cls, directory_path=None, relative=True, as_strings=False):
        ect = EventCreationTool()
        if directory_path is not None:
            ect.set_path_to_keys(directory_path, relative)
        return ect.get_own_feed_ids(as_strings)

    def __init__(self):
        self._hashing_algorithm = 0
        self._signing_algorithm = 0
        self._path_to_keys = os.getcwd()

    def set_path_to_keys(self, directory_path, relative=True):
        if relative:
            self._path_to_keys = os.path.join(os.getcwd(), directory_path)
        else:
            self._path_to_keys = directory_path

    def get_own_feed_ids(self, as_strings=False):
        (_, _, filenames) = next(os.walk(self._path_to_keys))
        list_of_strings = [filename[:len(filename) - 4] for filename in filenames if filename.endswith('.key')]
        if as_strings:
            return list_of_strings
        else:
            return [bytes.fromhex(feed_id) for feed_id in list_of_strings]

    def set_hashing_algorithm(self, hashing_algorithm):
        hashing_algorithm = hashing_algorithm.lower()
        if hashing_algorithm in self._HASH_INFO:
            self._hashing_algorithm = self._HASH_INFO[hashing_algorithm]
        else:
            raise HashingAlgorithmNotFoundException

    def set_signing_algorithm(self, signing_algorithm):
        signing_algorithm = signing_algorithm.lower()
        if signing_algorithm in self._SIGN_INFO:
            self._signing_algorithm = self._SIGN_INFO[signing_algorithm]
        else:
            raise SigningAlgorithmNotFoundException

    def get_supported_hashing_algorithms(self):
        return self._HASH_INFO.keys()

    def get_supported_signing_algorithms(self):
        return self._SIGN_INFO.keys()

    def generate_feed_and_create_first_event(self, app_name, master_feed_id):
        public_key = self.generate_feed()
        return self.create_first_event(public_key, app_name, master_feed_id)

    def generate_feed(self):
        private_key = secrets.token_bytes(32)
        if self._signing_algorithm == 0:
            signing_key = nacl.signing.SigningKey(private_key)
            public_key = signing_key.verify_key.encode()
        elif self._signing_algorithm == 1:
            public_key = secrets.token_bytes(32)
        else:
            raise SigningAlgorithmNotFoundException
        with open(os.path.join(self._path_to_keys, public_key.hex() + '.key'), 'wb') as file:
            file.write(private_key)
        return public_key

    def create_first_event(self, feed_id, app_name, master_feed_id):
        if not isinstance(master_feed_id, bytes):
            raise IllegalArgumentTypeException
        if isinstance(feed_id, str):
            feed_id = bytes.fromhex(feed_id)
        elif not isinstance(feed_id, bytes):
            raise IllegalArgumentTypeException
        content = Event.Content(app_name + "/MASTER", {'master_feed': master_feed_id})
        meta = Event.Meta(feed_id, 0, None, self._signing_algorithm, self._calculate_hash(content.get_as_cbor()))
        signature = self._calculate_signature(self._load_private_key(feed_id), meta.get_as_cbor())
        return Event.Event(meta, signature, content).get_as_cbor()

    def create_event(self, feed_id, last_sequence_number, hash_of_previous_meta,
                     content_identifier, content_parameter):
        if isinstance(feed_id, str):
            feed_id = bytes.fromhex(feed_id)
        elif not isinstance(feed_id, bytes):
            raise IllegalArgumentTypeException
        private_key = self._load_private_key(feed_id)
        content = Event.Content(content_identifier, content_parameter)
        meta = Event.Meta(feed_id, last_sequence_number + 1,
                          hash_of_previous_meta, self._signing_algorithm, self._calculate_hash(content.get_as_cbor()))
        signature = self._calculate_signature(private_key, meta.get_as_cbor())
        return Event.Event(meta, signature, content).get_as_cbor()

    def create_event_from_previous(self, previous_event, content_identifier, content_parameter):
        previous_event = Event.Event.from_cbor(previous_event)
        feed_id = previous_event.meta.feed_id
        last_sequence_number = previous_event.meta.seq_no + 1
        hash_of_previous_meta = self._calculate_hash(previous_event.meta.get_as_cbor())
        return self.create_event(feed_id, last_sequence_number, hash_of_previous_meta,
                                 content_identifier, content_parameter)

    def get_private_key_from_feed_id(self, feed_id):
        if isinstance(feed_id, bytes):
            feed_id = feed_id
        elif isinstance(feed_id, str):
            feed_id = bytes.fromhex(feed_id)
        else:
            raise IllegalArgumentTypeException(['bytes', 'str'])
        return self._load_private_key(feed_id)

    def get_private_key_from_event(self, event):
        if not isinstance(event, bytes):
            raise IllegalArgumentTypeException(['bytes'])
        feed_id = Event.Event.from_cbor(event).meta.feed_id
        return self._load_private_key(feed_id)

    def _load_private_key(self, feed_id):
        try:
            file = open(os.path.join(self._path_to_keys, feed_id.hex() + '.key'), 'rb')
        except FileNotFoundError:
            raise KeyFileNotFoundException
        else:
            private_key = file.read(32)
            file.close()
            return private_key

    def _calculate_hash(self, cbor_bytes):
        if self._hashing_algorithm == 0:
            return [self._hashing_algorithm, hashlib.sha256(cbor_bytes).digest()]
        else:
            raise HashingAlgorithmNotFoundException

    def _calculate_signature(self, private_key, cbor_bytes):
        if self._signing_algorithm == 0:
            signing_key = nacl.signing.SigningKey(private_key)
            return signing_key.sign(cbor_bytes).signature
        elif self._signing_algorithm == 1:
            return hmac.new(private_key, cbor_bytes, hashlib.sha256).digest()
        else:
            raise SigningAlgorithmNotFoundException


class FirstEventWasNotCreatedException(Exception):
    def __init__(self):
        super().__init__("You can not create the next event, please create a first event "
                         + "(using first_event() function) first.")


class FirstEventWasAlreadyCreatedException(Exception):
    def __init__(self):
        super().__init__("You can not create a first event, since it was already created.")


class EventFactory(EventCreationTool):

    def __init__(self, last_event=None, path_to_keys=None, path_to_keys_relative=True,
                 signing_algorithm='ed25519', hashing_algorithm='sha256'):
        super().__init__()
        if path_to_keys is not None:
            self.set_path_to_keys(path_to_keys, path_to_keys_relative)
        if last_event is not None:
            last_event = Event.Event.from_cbor(last_event)
            self.public_key = last_event.meta.feed_id
            self.sequence_number = last_event.meta.seq_no
            if last_event.meta.signature_info in self._SIGN_INFO.values():
                self._signing_algorithm = last_event.meta.signature_info
            else:
                raise SigningAlgorithmNotFoundException
            if last_event.meta.hash_of_content[0] in self._HASH_INFO.values():
                self._hashing_algorithm = last_event.meta.hash_of_content[0]
            else:
                raise HashingAlgorithmNotFoundException
            self.hash_of_previous_meta = self._calculate_hash(last_event.meta.get_as_cbor())
        else:
            self.public_key = self.generate_feed()
            self.sequence_number = -1
            self.hash_of_previous_meta = None
            self.set_signing_algorithm(signing_algorithm)
            self.set_hashing_algorithm(hashing_algorithm)

    def get_feed_id(self):
        return self.public_key

    def first_event(self, app_name, master_feed_id):
        if self.sequence_number != -1:
            raise FirstEventWasAlreadyCreatedException
        first_event = self.create_first_event(self.public_key, app_name, master_feed_id)
        self.hash_of_previous_meta = self._calculate_hash(Event.Event.from_cbor(first_event).meta.get_as_cbor())
        self.sequence_number += 1
        return first_event

    def next_event(self, content_identifier, content_parameter=None):
        if self.sequence_number == -1:
            raise FirstEventWasNotCreatedException
        new_event = self.create_event(self.public_key, self.sequence_number, self.hash_of_previous_meta,
                                      content_identifier, content_parameter)
        self.hash_of_previous_meta = self._calculate_hash(Event.Event.from_cbor(new_event).meta.get_as_cbor())
        self.sequence_number += 1
        return new_event

    def get_private_key(self):
        return self.get_private_key_from_feed_id(self.public_key)
