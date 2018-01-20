#!/usr/bin/env python

import sys


oldKey = None
count = 0

for line in sys.stdin:
    data_mapped = line.strip().split("\t")
    if len(data_mapped) != 2:
        continue

    thisKey, score = data_mapped

    if oldKey is not None and oldKey != thisKey:
        result = [oldKey, count]

        # hashtag
        if oldKey[0] == '#':
            print "{0}\t{1}".format('hashtag', result)
        # state
        else:
            print "{0}\t{1}".format('state', result)

        oldKey = thisKey
        count = 0
    oldKey = thisKey
    count += float(score)
