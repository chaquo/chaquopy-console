#!/usr/bin/env python3

# lib/feed.py
# Jan-Mar 2020 <christian.tschudin@unibas.ch>

import os

import event
import pcap
import crypto


class FEED:

    def __init__(self, fname, fid=None, signer=None,
                 create_if_notexisting=False):
        try:
            self.fname = fname
            self.fid = fid
            self.signer = signer
            self.cine = create_if_notexisting

            self.seq = 0
            self.pcap = pcap.PCAP(fname)
            self.hprev = None
            try:
                self.pcap.open('r')
                # find highest seq number:
                w = self.pcap.read_backwards(True)
                e = event.EVENT()
                e.from_wire(w)
                if fid != None and e.fid != fid:
                    print("feed ID mismatch:", e.fid, "instead of", fid)
                    self.pcap.close()
                    self.pcap = None
                    return
                self.fid, self.seq = e.fid, e.seq
                self.hprev = event.get_hash(e.metabits)
                self.pcap.close()
            except Exception as e:
                if not self.cine:
                    self.pcap = None
                    print(f"error opening file {fname}")
                else:
                    self.pcap.open('w')
                    self.pcap.close()
        except Exception as e:
            print("ERROR IN feed CONSTRUCTOR")
            _, _, tb = sys.exc_info()
            print(e)
            print("At line number {}".format(tb.tb_lineno))

    def _append(self, w): # blindly append the bytes in w to a log file
        p = self.pcap
        p.open('a')
        p.write(w)
        p.close()
        try:
            os.sync()
        except:
            pass
        self.seq += 1

    def write(self, c): # create new log extension with given content
        if self.seq == 0:
            self.hprev = None
        e = event.EVENT(fid=self.fid, seq=self.seq+1,
                        hprev=self.hprev, content=c)
        metabits = e.get_metabits(self.signer.get_sinfo())
        signature = self.signer.sign(metabits)
        w = e.to_wire(signature)
        self._append(w)
        self.hprev = event.get_hash(metabits)
        return w

    def is_valid_extension(self, e):
        if e.fid != self.fid or e.seq != self.seq+1:
            print(f"   out-of-seq (expected: {self.seq+1}, actual: {e.seq})")
            return False
        if isinstance(self.signer, crypto.ED25519):
            if e.sinfo != crypto.SIGNINFO_ED25519:
                print("   signature type mismatch")
                r = False
            else:
                r = crypto.ED25519.verify(e.fid, e.metabits, e.signature)
        elif isinstance(self.signer, crypto.HMAC256):
            if e.sinfo != crypto.SIGNINFO_HMAC_SHA256:
                print("   signature type mismatch")
                r = False
            else:
                r = crypto.HMAC256.verify(self.signer.get_private_key(),
                                          e.metabits, e.signature)
        else:
            r = False
        if not r:
            print("   invalid signature")
            return False
        if self.hprev != e.hprev:
            print(f"   invalid hash chaining: expected={self.hprev}, actual={e.hprev}")
            return False
        return True

    def ingest(self, e): # append event to log only if a valid extension
        # return False if failing
        try:
            if not self.is_valid_extension(e):
                print("   invalid extension")
                return False
            self._append(e.to_wire())
            self.hprev = event.get_hash(e.metabits)
            return True
        except Exception as x:
            print(x)
            pass
        print("   invalid packet")
        return False

    def __len__(self):
        return self.seq

    def __iter__(self):
        return FEED_ITER(self.fname)

class FEED_ITER:
    def __init__(self, fn):
        self.pcap = pcap.PCAP(fn)
        self.pcap.open('r')

    def __next__(self):
        pkt = self.pcap.read()
        if not pkt:
            self.pcap.close()
            raise StopIteration
        e = event.EVENT()
        e.from_wire(pkt)
        return e

# ----------------------------------------------------------------------


if __name__ == '__main__':

    import argparse
    import os
    import sys

    import crypto

    parser = argparse.ArgumentParser(description='BACnet feed tool')
    parser.add_argument('--keyfile')
    parser.add_argument('pcapfile', metavar='PCAPFILE')
    parser.add_argument('CMD', choices=['create','dump','append','check'])
    
    args = parser.parse_args()

    if args.CMD == 'dump':
        pcap.dump(args.pcapfile)

    elif args.CMD in ['create','append']:
        if args.keyfile == None:
            print("missing keyfile parameter")
            sys.exit()
        fid, signer = load_keyfile(args.keyfile)

        if args.CMD == 'create':
            try:
                os.remove(args.pcapfile)
            except:
                pass
            feed = FEED(args.pcapfile, fid, signer, True)
        else:
            feed = FEED(args.pcapfile, fid, signer)
        print("# enter payload of first event as a Python data structure, end with CTRL-D:")
        content = sys.stdin.read()
        feed.write(eval(content))

    elif args.CMD == 'check':
        if args.keyfile != None:
            fid, signer = load_keyfile(args.keyfile)
        else:
            fid, signer = None, None

        f = FEED(args.pcapfile, fid=fid, signer=signer)
        if f.pcap == None:
            sys.exit()
        f.seq = 0
        f.hprev = None
        print(f"Checking feed {f.fid.hex()}")
        for e in f:
            # print(e)
            if not f.is_valid_extension(e):
                print(f"-> event {f.seq+1}: chaining or signature problem")
            else:
                print(f"-> event {e.seq}: ok, content={e.content()}")
            f.seq += 1
            f.hprev = event.get_hash(e.metabits)

# eof
