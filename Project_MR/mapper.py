#!/usr/bin/env python

import sys
# import re
import json
import googlemaps


sys.path.append(".")


mood_dict = {}
NUM_API=1
API_KEY = ['AIzaSyBDhSjPyfDuhDXWu6IQVBVaWXZvFyesklU','AIzaSyCboEraLd2Rs4a9aJ7862UEBXRCNIl2aks',
           'AIzaSyBF783HUjBB6FUpuSyeqn-hfoRgbgU4Ln4','AIzaSyAg4JwdE9pZEyqKmUPNtjJW1-nVQArP3Aw',
           'AIzaSyAxvN1DTFwWjOPJ_1WGfrJTftKPS-elMAU','AIzaSyBOzXITcyEdNZ5LrJc_MLxshj3bEfv48HI']
COUNTRY = 'United States'
#Debug: bad_string = 0
body_str=None

gmaps = googlemaps.Client(key=API_KEY[NUM_API])
mood_file = open('AFINN-111.txt')
mood_file_emoticons = open('AFINN-emoticon-8.txt')

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'District of Columbia' : 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}

for line in mood_file:
    scores = line.split('\t')
    mood_dict[scores[0]] = float(scores[1])

for line in mood_file_emoticons:
    scores = line.split('\t')
    mood_dict[scores[0]] = float(scores[1])


for dataline in sys.stdin:
    record = json.loads(dataline, encoding="latin-1")

    body = record.get('text')
    place = record.get('place')

    #using place of tweet object
    if place:

        if place['full_name'] and place['country'] == COUNTRY:
            # Get state of US
            if place['place_type']=='city':
                place = place['full_name'].split(',')[1]
            elif place['place_type']=='admin':
                if ',' in place['full_name']:
                    place = us_state_abbrev[place['full_name'].split(',')[0]]
                else:
                    place = None
            else:
                place = None

        else:
            place = None

    # using coordinates places
    if not place:
        place = record.get('coordinates')

        if place:
            #print '---google'
            #print place['coordinates'][1]
            #print place['coordinates'][0]
            try:
                reverse_geocode_result = gmaps.reverse_geocode((place['coordinates'][1], place['coordinates'][0]))
            except:
                reverse_geocode_result = None
                place = None
                NUM_API = NUM_API + 1
                if NUM_API < len(API_KEY):
                    gmaps = googlemaps.Client(key=API_KEY[NUM_API])
                continue
            #print reverse_geocode_result

            if reverse_geocode_result:
                for type_place in reverse_geocode_result[0]['address_components']:
                    if 'administrative_area_level_1' in type_place['types']:
                        place = type_place['short_name']
                    if 'country' in type_place['types']:
                       if not type_place['long_name'] == COUNTRY:
                           place = None
                           break
            else:
                place = None

    if body:
        try:
            body_str = str(body.encode('utf-8'))
        except:
            # Debug: bad_string = bad_string + 1
            continue
    if body_str:
        text = body_str.split()
        #Other posibility using RE: re.split('#*\W+', body_str)

    if place and text:

        post_score = 0.0

        for word in text:
            if word:
                if word.lower() in mood_dict:
                    post_score += mood_dict[word.lower()]

                # hashtag
                if word[0] == '#':
                    print "{0}\t{1}".format(word.lower().strip(), 1)
        print "{0}\t{1}".format(place.strip(), post_score)
