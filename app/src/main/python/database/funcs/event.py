# Simple BACnet events wrapper
# Authors: Günes Aydin, Joey Zgraggen, Nikodem Kernbach
# VERSION: 1.0

import cbor


class Meta:

    # Create the Meta() object from scratch (for example if you create a new event)
    def __init__(self, feed_id, seq_no, hash_of_prev, signature_info, hash_of_content):
        self.feed_id = feed_id
        self.seq_no = seq_no
        self.hash_of_prev = hash_of_prev
        self.signature_info = signature_info
        self.hash_of_content = hash_of_content

    @classmethod
    def from_cbor(cls, meta):  # Read in a Meta() object from cbor format
        feed_id, seq_no, hash_of_prev, signature_info, hash_of_content = cbor.loads(meta)
        return Meta(feed_id, seq_no, hash_of_prev, signature_info, hash_of_content)

    def get_as_cbor(self):  # Get the cbor encoded version of the meta object
        return cbor.dumps([self.feed_id, self.seq_no, self.hash_of_prev, self.signature_info, self.hash_of_content])


class Content:

    # create content from scratch from identifier and parameter dictionary as specified in BACnet documentation
    def __init__(self, identifier, parameters):
        self.content = [identifier, parameters]

    @classmethod
    def from_cbor(cls, content):  # Read in a Content() object from cbor format
        identifier, parameters = cbor.loads(content)
        return Content(identifier, parameters)

    def get_as_cbor(self):  # Get the Content cbor encoded (as bytes() python object)
        return cbor.dumps(self.content)


class Event:

    # Create Event from scratch. NOTE!!!: meta and content parameters must be Meta() and Content() objects! (see above)
    def __init__(self, meta, signature, content):
        self.meta = meta
        self.signature = signature
        self.content = content

    # parameter event: cbor encoded feed event
    @classmethod
    def from_cbor(self, event):  # Read in an Event from cbor format (parameter is bytes()), creates a new Event object
        meta, signature, content = cbor.loads(event)
        meta = Meta.from_cbor(meta)
        content = Content.from_cbor(content)
        return Event(meta, signature, content)

    def get_as_cbor(self):  # return an event cbor encoded as bytes() python object
        return cbor.dumps([self.meta.get_as_cbor(), self.signature, self.content.get_as_cbor()])
