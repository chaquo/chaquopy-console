#!/usr/bin/env python3

# lib/crypto.py


import hmac
import nacl.signing
import nacl.exceptions
import os

# signature info
SIGNINFO_ED25519     = 0
SIGNINFO_HMAC_SHA256 = 1


class ED25519:

    def __init__(self, privateKey = None):
        self.sinfo = SIGNINFO_ED25519
        try:
            self.sk = nacl.signing.SigningKey(privateKey)
        except:
            self.sk = None

    def get_sinfo(self):
        return self.sinfo

    def create(self):
        self.sk = nacl.signing.SigningKey.generate()

    def sign(self, blob):
        signed = self.sk.sign(blob)
        return signed.signature

    def get_public_key(self):
        return bytes(self.sk.verify_key)

    def get_private_key(self):
        return bytes(self.sk)

    @staticmethod
    def verify(public, blob, signature=None):
        """
        :param public: public key as bytes
        :param blob: Binary Large Object
        :param signature: The signature of the blob to verify against. If the value of blob is the concated signature and blob, this parameter can be None.
        :return: True when the Blob is successfully verified
        """
        verify_key = nacl.signing.VerifyKey(public)
        try:
            verify_key.verify(blob, signature)
        except nacl.exceptions.BadSignatureError:
            return False
        else:
            return True

    def as_string(self):
        return str({'type': 'ed25519',
                    'public': self.get_public_key().hex(),
                    'private': self.get_private_key().hex()})


class HMAC256:
    
    def __init__(self, sharedSecret = None, fid=None):
        self.sinfo = SIGNINFO_HMAC_SHA256
        self.ss = sharedSecret
        self.fid = fid

    def get_sinfo(self):
        return self.sinfo

    def create(self):
        self.ss = os.urandom(16)
        self.fid = os.urandom(32)

    def sign(self, blob):
        h = hmac.new(self.ss, blob, 'sha256')
        return h.digest()

    def get_feed_id(self):
        return self.fid

    def get_private_key(self):
        return self.ss

    @staticmethod
    def verify(secret, blob, signature=None):
        """
        :param blob: Binary Large Object
        :param signature: The signature of the blob to verify against. If the value of blob is the concated signature and blob, this parameter can be None.
        :return: True when the Blob is successfully verified
        """
        if signature == None:
            signature = blob[:32]
            blob = blob[32:]
        h = HMAC256(secret)
        return hmac.compare_digest(h.sign(blob), signature)

    def as_string(self):
        return str({'type': 'hmac_sha256',
                    'feed_id': self.get_feed_id().hex(),
                    'private': self.get_private_key().hex()})

# ---------------------------------------------------------------------------

def run(hmac=None, test=None):
	if test == None:
		if hmac:
			h = HMAC256()
			h.create()
			print("# new HMAC_SHA256 key: share it ONLY with trusted peers")
			print('{\n  '+(',\n '.join(h.as_string().split(','))[1:-1])+'\n}')
		else:
			key_pair = ED25519()
			key_pair.create()
			print("# new ED25519 key pair: ALWAYS keep the private key as a secret")
			print('{\n  '+(',\n '.join(key_pair.as_string().split(','))[1:-1])+'\n}')
	else:
		if hmac:
			print("Creating an HMAC_SHA256 key, testing signing")
			
			# generate random key
			h = HMAC256()
			h.create()
			print("shared key is", h.as_string())
			secret = h.get_private_key()			
			msg = "hello world test 1234 / hmac_sha256".encode()
			signature = h.sign(msg)			
			print("verify1:", HMAC256.verify(secret, msg, signature))
			print("verify2:", HMAC256.verify(secret, signature+msg))
		else:
			print("Creating an ED25519 key pair, testing signing")

			# generate random key pair
			key_pair = ED25519()
			key_pair.create()
			print("key pair is", key_pair.as_string())
			secret = key_pair.get_private_key()

			msg = "hello world test 1234 / ed25519".encode()
			signature = key_pair.sign(msg)

			print("verify1:", ED25519.verify(key_pair.get_public_key(),
                                             msg, signature))


			# use previously generated (secret) key, test with concatenated sign+msg
			kp2 = ED25519(secret)
			print("verify2:", ED25519.verify(kp2.get_public_key(), signature+msg))


if __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser(description='BACnet key generation')
    parser.add_argument('--hmac', action='store_true',
                        help='choose HMAC_SHA256 instead of ED25519 (default)')
    parser.add_argument('test', nargs='?',
                        help='run test code instead generating a key(pair)')
    args = parser.parse_args()

    if args.test == None:
        # default action: create a key (pair) and pretty print the key values:
        if args.hmac:
            h = HMAC256()
            h.create()
            print("# new HMAC_SHA256 key: share it ONLY with trusted peers")
            print('{\n  '+(',\n '.join(h.as_string().split(','))[1:-1])+'\n}')
        else:
            key_pair = ED25519()
            key_pair.create()
            print("# new ED25519 key pair: ALWAYS keep the private key as a secret")
            print('{\n  '+(',\n '.join(key_pair.as_string().split(','))[1:-1])+'\n}')
    else:
        if args.hmac:
            print("Creating an HMAC_SHA256 key, testing signing")
            
            # generate random key
            h = HMAC256()
            h.create()
            print("shared key is", h.as_string())
            secret = h.get_private_key()

            msg = "hello world test 1234 / hmac_sha256".encode()
            signature = h.sign(msg)

            print("verify1:", HMAC256.verify(secret, msg, signature))
            print("verify2:", HMAC256.verify(secret, signature+msg))
        else:
            print("Creating an ED25519 key pair, testing signing")

            # generate random key pair
            key_pair = ED25519()
            key_pair.create()
            print("key pair is", key_pair.as_string())
            secret = key_pair.get_private_key()

            msg = "hello world test 1234 / ed25519".encode()
            signature = key_pair.sign(msg)

            print("verify1:", ED25519.verify(key_pair.get_public_key(),
                                             msg, signature))


            # use previously generated (secret) key, test with concatenated sign+msg
            kp2 = ED25519(secret)
            print("verify2:", ED25519.verify(kp2.get_public_key(), signature+msg))

# eof
