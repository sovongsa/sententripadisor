#!/usr/bin/env python
# encoding: utf-8
"""

 @contact: sovongsa.ly@gmail.com
"""


class WatsonAssistantCreds(object):
    username = '{Watson Assistant Username}',
    password = '{Watson Assistant Password}',
    version = '2018-07-10',
    workspace_id = '{workspaceid}'

class WatsonNaturalLanguageProcessing(object):
    version='2018-03-16',
    username='{Watson NPL username}',
    password='{Watson NPL password}'

GOOGLE_API_KEY = '{Google API Key}'

GOOGLE_PLACE_URL = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={0}&inputtype=textquery&fields=photos,formatted_address,name,rating,opening_hours,geometry&key={1}'
GOOGLE_IMAGE_URL = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={0}&key={1}'
GOOGLE_NEARBY_AIRPORT='https://maps.googleapis.com/maps/api/place/textsearch/json?query={0}&key={1}&type=airport'
GOOGLE_NEARBY_AIRPORT_BY_LAT_LNG = "https://maps.googleapis.com/maps/api/place/textsearch/json?&location={0},{1}&type=airport&key={2}"
GOOGLE_NEARBY_HOTEL_BY_LAT_LNG = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={0},{1}&radius=10000&key={2}&type=lodging"
EXPEDIA_CHEAPEST_FLIGHT =  "https://apim.expedia.com/x/flights/overview"
EXPEDIA_API_KEY = '{Expedia API}'
EXPEDIA_THINGS_TODO='https://apim.expedia.com/x/activities/search?location={0}'
EXPEDIA_CAR_RENTALS='https://apim.expedia.com/x/cars/search?pickupdate={0}&dropoffdate={1}&pickuplocation={2}&dropofflocation={3}&sort=price&limit=25'
GOOGLE_GET_LOCATION_GEO='https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'