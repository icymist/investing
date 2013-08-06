#! /usr/bin/env python

import re
from glob import glob
from multiprocessing import cpu_count, Pool

ncpus = cpu_count()
p = Pool(ncpus)

m = re.compile(r'BSE: \d{6}')

def get_bsecode(f):
    #mobj = re.match(r'BSE: (\d{6})', open(f).read())
    matches = m.findall(open(f).read())
    if matches:
        return matches[0].split()[-1]
    else:
        return None

files = glob('tmp/stock_quote_pages/*.html')
#bsecodes = p.map(get_bsecode, files)
bsecodes = [get_bsecode(f) for f in files]

for bsecode, f in zip(bsecodes, files):
    print bsecode, f
