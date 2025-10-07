#!/usr/bin/env python

import sys
import glob

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: %s region_file" % sys.argv[0])
        sys.exit(1)
    ptsrc = open(sys.argv[1], "r")
    annuli = open("annuli_all.reg", 'r')

    for i, region in enumerate(annuli.readlines()):
        if region.startswith("#"): continue
        elif region.startswith("annulus"):
            reg = open('region'+str(i-1)+'.reg', 'w')
            reg.write(region)
            reg.close()

    for reg in glob.glob("region*.reg"):
        regfile = open(reg, "a")
        #regfile.write('#Excluded regions' + '\n')
        ptsrc.seek( 0, 0 )
        for line in ptsrc:
            if line.startswith("#"): continue
            elif line.startswith("-"): regfile.write( line )
            else: regfile.write( "-" + line )
        regfile.close()

    ptsrc.close()
    annuli.close() 
