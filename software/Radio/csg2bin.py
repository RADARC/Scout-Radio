#
# create patchcomp.bin from patch.csg
# "compressed" version of patch.csg
#
import os

def decodecompbin(cmpbytes):
    length = int(cmpbytes[0])

    specials=[]
    for i in range(0,length*2,2):
        special_idx = i + 1
        special = int.from_bytes(cmpbytes[special_idx:special_idx+2],"big")
        specials.append(special)

    the_rest = cmpbytes[1 + length*2:]

    assert len(the_rest) % 7 == 0

    return (length, specials, the_rest)

def readcsgfile(csgfilespec):
    result = bytearray()
    specials = []
    line_number = 0

    with open(csgfilespec,"r") as csgfile:
        for line in csgfile.readlines():
            if line.startswith("#"):
                continue

            chunkstrlist = line.strip().split(',')

            chunk = [int(item, 16) for item in chunkstrlist]

            result.extend(bytearray(chunk[1:]))

            if chunk[0] == 0x15:
                specials.append(line_number)

            line_number += 1

    return (result, specials)

def writebinfile(outfile, specials, body):
    header=bytearray([len(specials)])

    for d in specials:
        # endian is arbitrary
        #print(d.to_bytes(2, "big"))
        header.extend(d.to_bytes(2, "big"))

    #print(result)
    finalbytearray = header + body

    # sanity
    (special_len, specials, body) = decodecompbin(finalbytearray)

    print(special_len, specials)

    with open(outfile,"wb") as compressed_binpatchfile:
        compressed_binpatchfile.write(finalbytearray)

if __name__ == "__main__":
    infile = "patch.csg"
    outfile = os.path.splitext(infile)[0]+"comp.bin"

    # internalise patch.csg
    (body, specials) = readcsgfile(infile)

    assert len(specials) < 256
    #print([hex(x) for x in body])

    #
    # create a binary file:
    # -- number of "specials"
    # -- specials as 16 bit quantities
    # -- seven byte arrays consecutively as the body
    #
    writebinfile(outfile, specials, body)
        
