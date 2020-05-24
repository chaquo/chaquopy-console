import Event  # Our representation of an feed event, please refer to Event.py
import hashlib  # Comes with python
import hmac  # Comes with python
import secrets  # Comes with python
import nacl.signing  # install with 'pip install pynacl'
import nacl.encoding

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# THIS FILE IS OUT OF DATE. PLEASE REFER TO README.md FOR A NEW OPTION TO CREATE EVENTS
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# !!! For the code to work your also need to install cbor2 (This is used inside Event.py) !!!
# Install with: 'pip install cbor2'

# These are the currently supported signing/hashing algorithms. Contact us if you need another one!
SIGN_INFO = {'ed25519': 0, 'hmac_sha256': 1}
HASH_INFO = {'sha256': 0}

if __name__ == "__main__":

    print()
    # In the following we will create a feed_id and two first events with dummy content:
    # For the signatures and thus the public key you can choose from the following two algorithms:
    # 'ed25519' OR 'hmac_sha256'
    # When you want to use the 'hmac_sha256' algorithm, you will need to exchange a private key with all
    # recipients over a secure channel (qr code or whatever), but not over bacnet since everybody will be able
    # to forge your messages
    # Please contact us if you need another algorithm!
    # The following example used 'ed25519' for the signatures
    # !!! At the bottom of the file is an example how to sign using hmac_sha256 !!!

    # First, we create a public key (feed id) and a private key (used to sign messages)
    # Therefore, we create a random bytes() object of length 32 (32 random bytes)
    private_key = secrets.token_bytes(32)
    print("The private key is:", private_key)
    signing_key = nacl.signing.SigningKey(private_key)  # contains both
    # We can extract the public key as follows (already converting it to bytes() object)
    public_key_feed_id = signing_key.verify_key.encode(encoder=nacl.encoding.HexEncoder)
    print("The public key is:", str(public_key_feed_id).split("'")[1])  # conv. bytes to str of hex numbers for printing
    print()
    # If you need to restart your app, just save the private_key inside the database or a file and then reload it.
    # You can recreate the object as on line 26 using the old private_key, to sign events again
    # (The signing_key is an object from the pynacl library that you need to sign messages (i.e. the meta headers))

    # Now, let's create some dummy content for a first event
    content = Event.Content('whateverapp/whateveraction', {'somekey': 'somevalue', 'someotherkey': 753465734265})

    # In the meta data of a event, we have to specify the hash of the meta data of the previous event and of
    # the current content. Therefore we need a hashing algorithm. Currently we support only the 'sha256' algorithm
    # If you need another algorithm, please contact us
    # Let's calculate the hash of our content:
    hash_of_content = hashlib.sha256(content.get_as_cbor()).hexdigest()

    # Since this is our first event, and there is no previous one, the hash of the previous meta data is just None
    hash_of_prev = None

    # Now we have everything to build our meta header (as specified on the repository):
    meta = Event.Meta(public_key_feed_id, 0, hash_of_prev, SIGN_INFO['ed25519'], (HASH_INFO['sha256'], hash_of_content))

    # Now lets sign the meta header and therewith create a signature
    signature = signing_key.sign(meta.get_as_cbor())._signature  # ignore the access of prot. member, works just fine!

    # Now lets combine the meta header, signature and content to one cbor binary encoded event:
    event = Event.Event(meta, signature, content).get_as_cbor()
    # !!!! THIS CBOR-ENCODED EVENT CAN BE PASSED TO THE DATABASE AS BYTES EVENT (IT IS ACTUALLY A BYTES() PYTHON OBJECT)

    # Just for visualisation this is how this looks like:
    print("meta header as cbor:", meta.get_as_cbor())
    print("signature:", signature)
    print("content as cbor:", content.get_as_cbor())
    print("The complete event as cbor:", event)
    print()

    # Now lets create a valid second event for this feed id
    second_dummy_content = Event.Content('someapp/somecommand', {'firstkey': 432, 'second': 'LOL'})
    hash_of_second_content = hashlib.sha256(second_dummy_content.get_as_cbor()).hexdigest()
    hash_of_first_meta_header = hashlib.sha256(meta.get_as_cbor()).hexdigest()
    second_meta = Event.Meta(public_key_feed_id,
                             1,  # second entry, since seq_no is 1 (0 + 1)
                             (HASH_INFO['sha256'], hash_of_first_meta_header),  # in a tuple this time, as spec. on rep.
                             SIGN_INFO['ed25519'],
                             (HASH_INFO['sha256'], hash_of_second_content))

    # Create signature for second event
    second_signature = signing_key.sign(second_meta.get_as_cbor())._signature

    # Combine to one cbor encoded second event:
    second_event = Event.Event(second_meta, second_signature, second_dummy_content).get_as_cbor()
    # !!!! THIS CBOR-ENCODED EVENT CAN BE PASSED TO THE DATABASE AS BYTES EVENT (IT IS ACTUALLY A BYTES() PYTHON OBJECT)
    print("The second complete event as cbor:", second_event)

    # !!! hmac_sha256
    # If you want to use the hmac_sha256 signing algorithm, you can use the following code:
    # Generate private key: (Unlike in 'ed25519', you have to share this key with all recipients through a safe channel)
    # ! If the recipient does not have this key, he will reject the events!
    private_key = secrets.token_bytes(32)
    # sign the meta header of the first event
    signature = hmac.new(private_key, meta.get_as_cbor(), hashlib.sha256).hexdigest()
    # The signature_info now would be: (as specified on the repository)
    signature_info = 'hmac_sha256'

# !!!!! THIS IS JUST FOR DEMO PURPOSES IN THE WORKSHOP. AS APPLICATION LEVEL GROUP NEVER CREATE A .pcap FILE !!!!!
if __name__ == "__main__":
    import PCAP
    PCAP.PCAP.write_pcap('whateverfilename', [event, second_event])
