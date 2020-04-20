#!/usr/bin/env python3

# lib/feed.py
# Jan 2020 <christian.tschudin@unibas.ch>

''' event data structure (="log entry")

  +-event------------------------------------------------------------------+
  | +-meta---------------------------------------+                         |
  | | feed_id, seq_no, h_prev, sign_info, h_cont |, signature, opt_content |
  | +--------------------------------------------+                         |
  +------------------------------------------------------------------------+

  event :== cbor( [ meta, signature, opt_content ] )

  meta  :== cbor( [ feed_id, seq_no, h_prev, sign_info, h_cont ] )

  h_prev         :== [hash_info, "hash value of prev event's meta field"]
  signature      :== "signature of meta"
  h_cont         :== [hash_info, "hash value of opt_content"]

  sign_info:     enum (0=ed25519)
  hash_info:     enum (0=sha256)

  opt_content    :== cbor( data )  # must be bytes so we can compute a hash)
  
'''

import hashlib
import cbor2

import crypto

# hash info
HASHINFO_SHA256      = 0
HASHINFO_SHA512      = 1


# ---------------------------------------------------------------------------

def serialize(ds):
    return cbor2.dumps(ds)

def deserialize(s):
    return cbor2.loads(s)

def get_hash(blob):
    return hashlib.sha256(blob).digest()

# ---------------------------------------------------------------------------

class EVENT:

    def __init__(self, fid=None, seq=1, hprev=None, content=None):
        self.wire, self.metabits, self.sinfo  = None, None, -1
        self.fid, self.seq, self.hprev        = fid, seq, hprev
        self.contbits = serialize(content)

    def from_wire(self, w):
        self.wire = w
        e = deserialize(w)
        self.metabits, self.signature = e[:2]
        self.contbits = None if len(e) < 2 else e[2]
        self.fid, self.seq, self.hprev, self.sinfo, self.hcont = \
                                                  deserialize(self.metabits)[:5]

    def get_metabits(self, sign_info):
        self.sinfo = sign_info
        meta = [self.fid, self.seq, self.hprev, self.sinfo,
                [HASHINFO_SHA256, get_hash(self.contbits)]]
        self.metabits = serialize(meta)
        return self.metabits

    def to_wire(self, signature):
        # must be called after having called get_metabits()
        if self.wire != None:
            return self.wire
        self.signature = signature
        self.wire = serialize([ self.metabits, signature, self.contbits ])
        return self.wire

    def chk_content(self):
        return self.hcont == get_hash(self.contbits)

    def content(self):
        return deserialize(self.contbits)

    def __str__(self):
        e = deserialize(self.wire)
        e[0] = deserialize(e[0])
        e[2] = deserialize(e[2])
        return "e - " + str(e)

    pass

# ----------------------------------------------------------------------
        
# eof
