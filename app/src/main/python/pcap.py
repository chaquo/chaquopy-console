#!/usr/bin/env python3

# lib/pcap.py
# Nov 2019, Mar 2020 <christian.tschudin@unibas.ch>


# import fcntl            # uncomment the LOCK_ calls for concurrent processes

import cbor
import hashlib

class PCAP:

    def __init__(self, fname, rd_offset=0):
        self.fn = fname
        self.f = None
        self.rd_offset = rd_offset

    def _wr_typed_block(self, t, b):
        self.f.write(t.to_bytes(4,'big'))
        m = len(b) % 4
        if m > 0:
            b += b'\x00' * (4-m)
        l = (8 + len(b) + 4).to_bytes(4,'big')
        self.f.write(l+b+l)
        self.f.flush()

    def open(self, mode, offset=0): # modes: "r,w,a"
        if mode == 'a':
            mode = 'r+'
        if mode == 'r+':
            try:
                f = open(self.fn, mode)
                f.close()
            except: # if not existing we have to create the file
                mode = 'w'
        self.f = open(self.fn, mode + 'b')
        # if mode[-1] in 'w+':
        #     fcntl.flock(self.f, fcntl.LOCK_EX)
        # else:
        #     fcntl.flock(self.f, fcntl.LOCK_SH)
        if mode == 'w':
            # write initial sect block
            self._wr_typed_block(int(0x0A0D0D0A),
                     int(0x1A2B3C4D).to_bytes(4, 'big') + \
                     int(0x00010001).to_bytes(4, 'big') + \
                     int(0x7fffffffffffffff).to_bytes(8, 'big'))
            # write interface description block
            self._wr_typed_block(1,
                                 (99).to_bytes(2,'big') + \
                                 b'\00\00\00\00\00\00')
        elif mode in ['r', 'r+']:
            self.f.seek(48, 0)
        else:
            self.f.seek(offset, 0)
        self.rd_offset = self.f.tell()

    def close(self):
        if self.f:
            # fcntl.flock(self.f, fcntl.LOCK_UN)
            self.f.close()
            self.f = None

    def read(self): # returns packets, or None
        w = None
        # print('pcap read lim=', lim)
        while True:
            self.last_read_offset = self.f.tell()
            # print(f"  read at {self.rd_offset}/{self.f.tell()}")
            t = int.from_bytes(self.f.read(4), 'big')
            # print(f"typ={t}")
            l = int.from_bytes(self.f.read(4), 'big')
            # print(f"t={t} len={l}")
            if l < 12:
                break
            # print("  read typ/len at", self.last_read_offset, t, l-12)
            b = self.f.read(l-12)
            _ = self.f.read(4)
            if t == 3:
                l = int.from_bytes(b[:4], 'big')
                w = b[4:4+l]
                break
            self.rd_offset += 4+4+l-12
        self.rd_offset = self.f.tell()
        return w

    def read_backwards(self, start_at_end=False):
        if start_at_end:
            self.f.seek(0, 2)
            self.rd_offset = self.f.tell()
        while self.rd_offset > 48:
            self.f.seek(-4, 1)
            l = int.from_bytes(self.f.read(4), 'big')
            self.f.seek(-l, 1)
            t = int.from_bytes(self.f.read(4), 'big')
            self.f.seek(-4, 1)
            self.rd_offset -= l
            if t == 3:
                w = self.read()
                self.rd_offset -= l
                return w
        return None

    def __iter__(self): # only one thread can iter through the file
        return self

    def __next__(self):
        pkt = self.read()
        if not pkt:
            self.rd_offset = 48
            raise StopIteration
        return pkt

    def write(self, pkt):
        self.f.seek(0,2)
        self._wr_typed_block(3, len(pkt).to_bytes(4,'big') + pkt)

# ----------------------------------------------------------------------

def base64ify(d):
    if type(d) == list:
        return [base64ify(x) for x in d]
    if type(d) == dict:
        return {base64ify(k):base64ify(v) for k,v in d.items()}
    if type(d) in [bytes, bytearray]:
        # s = binascii.b2a_base64(d)[:-1].decode('ascii')
        s = d.hex()
        return s[0:6] + '..' + s[-6:]
    return d

def dump(fname):
    p = PCAP(fname)
    p.open('r')
    s = ""
    for w in p:
        # here we apply our knowledge about the event/pkt's internal struct
        e = cbor.loads(w)
        href = hashlib.sha256(e[0]).digest()
        e[0] = cbor.loads(e[0])
        # rewrite the packet's byte arrays for pretty printing:
        e[0] = base64ify(e[0])
        fid = e[0][0]
        seq = e[0][1]
        if e[2] != None:
            e[2] = cbor.loads(e[2])
        #s += f"** fid={fid}, seq={seq}, ${len(w)} bytes" + "\n"
        #s += f"   hashref={href.hex()}" + "\n"
        #s += f"   content={e[2]}" + "\n"
        s += f"content={e[2]}" + "_" + f"seq={seq}" + "_"
    p.close()
    return s



# ----------------------------------------------------------------------

if __name__ == '__main__':
    import binascii
    import cbor
    import hashlib
    import sys

    # sys.path.insert(1, 'lib')
    dump(sys.argv[1])

# eof
