#
# based on https://forum.micropython.org/viewtopic.php?t=5274
#
class bitfield():
    def __init__(self, bytes):
        self.m_val = bytes
        self.m_bitnames = {}

    def fielddef(self, bitname, bitpos, bitlen=1, bitdefval=0):
        self.m_bitnames[bitname] = (bitpos, bitlen, bitdefval)

    def transitem(self, n):
        # manual length specified
        if isinstance(n, tuple):
            (bitid, fieldlen) = n
        else:
            bitid = n
            fieldlen = 1

        if isinstance(bitid, str):
            (bpos, bitlen, bitdefval) = self.m_bitnames[bitid]
        else:
            bpos = bitid
            bitlen = fieldlen
            bitdefval = 99

        return (bpos, bitlen, bitdefval)

    def __getitem__(self, n):
        (bpos, fieldlen, _bitdefval) = self.transitem(n)

        startval = self.m_val >> bpos

        acc = 0
        for i in range(fieldlen):
            acc += startval & (1 << i)

        return acc


    def __setitem__(self, n, vv):
        (bpos, fieldlen, _bitdefval) = self.transitem(n)

        for i in range(fieldlen):
            v = vv & (1 << i)

            if v:
                self.m_val |= v << bpos
            else:
                self.m_val &= ~(v << bpos)


if __name__ == "__main__":
    b = bitfield(1)
    b.fielddef("byte",0,8)
    b.fielddef("field0",0,2)
    b.fielddef("field2",1,1)

    b.fielddef("topnibble",4,4)

    b["field0"]=3
    b["topnibble"]=15
    print(b[0])
    print(b[0, 2])
    print(b["byte"])

    print(b["field2"])
