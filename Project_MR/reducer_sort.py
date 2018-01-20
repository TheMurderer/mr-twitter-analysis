#!/usr/bin/env python

import sys
import operator

scoreTotal = 0
scoreTotalHashtag =0

oldKey = None
oldHashTag=None

locations_dict = {}
hashtag_dict = {}
result = []

for line in sys.stdin:
    data_mapped = line.strip().split("\t")
    if len(data_mapped) != 2:
        continue

    thisKey, score = data_mapped
    transform_value = score[1:len(score)-1]
    result = transform_value.split(',')


    #hashtag
    if thisKey =='hashtag':
        if oldHashTag is not None and oldHashTag != thisKey:
            hashtag_dict[result[0]] = scoreTotalHashtag
            oldHashTag = result[0]
            scoreTotalHashtag = 0
        oldHashTag = result[0]
        scoreTotalHashtag+=1

    # locations
    else:

        if oldKey is not None and oldKey != thisKey:
            locations_dict[result[0]] = scoreTotal
            oldKey = result[0]
            scoreTotal = 0

        oldKey = result[0]
        scoreTotal += float(result[1])

if oldHashTag is not None:
    hashtag_dict[result[0]] = scoreTotalHashtag

if oldKey is not None:
    locations_dict[result[0]] = scoreTotal

print '----------------------- RESULTS BY LOCATIONS -----------------------'
sorted_locations = sorted(locations_dict.iteritems(), key=operator.itemgetter(1))
for location in sorted_locations:
    print "{0}\t{1}".format(location[0], location[1])

print '----------------------- RESULTS BY HASHTAG -----------------------'
sorted_hashtag = sorted(hashtag_dict.iteritems(), key=operator.itemgetter(1))
for hashtag in sorted_hashtag[-10:]:
    print "{0}\t{1}".format(hashtag[0], hashtag[1])