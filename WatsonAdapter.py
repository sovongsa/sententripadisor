#!/usr/bin/env python
# encoding: utf-8
"""
 @contact: sovongsa.ly@gmail.com
"""

from config import WatsonAssistantCreds, WatsonNaturalLanguageProcessing
import json
import requests
import config
import watson_developer_cloud
import datetime
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
    import Features, EntitiesOptions, KeywordsOptions
from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring

place_entity_type = ['location', 'facility']


class WatsonNaturalLanguageProcessingAdapter(object):
    natural_language_understanding = None

    def __init__(self):
        self.natural_language_understanding = NaturalLanguageUnderstandingV1(
            version=''.join(WatsonNaturalLanguageProcessing.version),
            username=''.join(WatsonNaturalLanguageProcessing.username),
            password=''.join(WatsonNaturalLanguageProcessing.password)
        )

    def analyze(self, sentence):
        response_places = []
        response = self.natural_language_understanding.analyze(
            text=sentence['input'],
            features=Features(
                entities=EntitiesOptions(
                    emotion=True,
                    sentiment=True,
                    limit=1),
                keywords=KeywordsOptions(
                    emotion=True,
                    sentiment=True,
                    limit=1)))

        # print(json.dumps(response, indent=2))
        '''
        places
        '''
        if len(response['entities']) > 0 and str(response['entities'][0]['type']).lower() in place_entity_type:
            new_input = {}
            destination_name = response['keywords'][0]['text']
            new_input['current_lat'] = sentence['current_lat']
            new_input['current_lng'] = sentence['current_lng']
            new_input['destination_name'] = destination_name
            location_request = requests.get(
                url=config.GOOGLE_GET_LOCATION_GEO.format(destination_name, config.GOOGLE_API_KEY))
            location_geo = json.loads(location_request.content)['results'][0]['geometry']['location']
            new_input['destination_lat'] = location_geo['lat']
            new_input['destination_lng'] = location_geo['lng']
            return get_recommended_trip(new_input)
        else:
            keyword = response['keywords'][0]['text']
            message_res = WatsonWatsonAssistantAdapter().message(keyword)
            places = message_res['output']['text']
            for place in places:
                google_places_response = requests.get(url=config.GOOGLE_PLACE_URL.format(place, config.GOOGLE_API_KEY))
                google_place = json.loads(google_places_response.content)['candidates'][0]
                place_element = {}
                place_element['name'] = google_place['name']
                place_element['image'] = config.GOOGLE_IMAGE_URL.format(
                    google_place['photos'][0]['photo_reference'], config.GOOGLE_API_KEY)
                place_element['rating'] = google_place['rating']
                place_element['lat'] = google_place['geometry']['location']['lat']
                place_element['lng'] = google_place['geometry']['location']['lng']
                response_places.append(place_element)

            print response_places
            response_dict = {}
            response_dict['places'] = response_places
            response_dict['trips'] = {}
        return response_dict


class WatsonWatsonAssistantAdapter(object):
    assistant = None

    def __init__(self):
        self.assistant = watson_developer_cloud.AssistantV1(
            username=''.join(WatsonAssistantCreds.username),
            password=''.join(WatsonAssistantCreds.password),
            version=''.join(WatsonAssistantCreds.version)
        )

    def message(self, text):
        response = self.assistant.message(
            workspace_id=WatsonAssistantCreds.workspace_id,
            input={
                'text': text
            }
        )

        return response


def get_recommended_trip(input):
    response_dict = {}
    response_dict['places'] = []
    current_lat = input['current_lat']
    current_lng = input['current_lng']
    destination_lat = input['destination_lat']
    destination_lng = input['destination_lng']

    '''
    get flights for trip
    '''
    destination_name = input['destination_name']

    nearby_current_location_aiport = requests.get(
        config.GOOGLE_NEARBY_AIRPORT_BY_LAT_LNG.format(current_lat, current_lng, config.GOOGLE_API_KEY))
    nearby_aiport_name = json.loads(nearby_current_location_aiport.content)['results'][0]['name']

    nearby_destination_location_aiport = requests.get(
        config.GOOGLE_NEARBY_AIRPORT_BY_LAT_LNG.format(destination_lat, destination_lng, config.GOOGLE_API_KEY))
    distination_aiport_name = json.loads(nearby_destination_location_aiport.content)['results'][0]['name']
    distination_airport_code = WatsonWatsonAssistantAdapter().message(distination_aiport_name)['output']['text'][0]

    orgin_airport_code = WatsonWatsonAssistantAdapter().message(nearby_aiport_name)['output']['text'][0]

    now = datetime.datetime.now()
    flight_request_body = {
        "MessageHeader": {"ClientInfo": {"DirectClientName": "Hackathon"}, "TransactionGUID": ""},
        "tpid": 1, "eapid": 0,
        "PointOfSaleKey": {"JurisdictionCountryCode": "USA", "CompanyCode": "10111", "ManagementUnitCode": "1010"},

        "OriginAirportCodeList": {
            "AirportCode": [orgin_airport_code]
        },
        "DestinationAirportCodeList": {
            "AirportCode": [distination_airport_code]
        },

        "FareCalendar": {
            "StartDate": now.strftime("%Y-%m-%d"),
            "DayCount": 60
        }
    }

    flights = requests.post(url=config.EXPEDIA_CHEAPEST_FLIGHT, json=flight_request_body,
                            headers={"key": config.EXPEDIA_API_KEY})

    flights = json.loads(flights.content)['FareCalendar']['AirOfferSummary']

    '''
    get hotels for the trips
    '''
    hotels_response = requests.get(
        url=config.GOOGLE_NEARBY_HOTEL_BY_LAT_LNG.format(destination_lat, destination_lng, config.GOOGLE_API_KEY))

    hotels_response = json.loads(hotels_response.content)['results']

    hotels_list = []

    for hotel in hotels_response:
        hotel_element = {}
        hotel_element["name"] = hotel['name']
        hotel_element["rating"] = 'N/A' if 'rating' not in hotel else hotel['rating']
        hotel_element[""] = hotel['vicinity']
        hotel_element['image'] = '' if 'photos' not in hotel else config.GOOGLE_IMAGE_URL.format(
            hotel['photos'][0]['photo_reference'], config.GOOGLE_API_KEY)
        hotels_list.append(hotel_element)

    '''
    get things to do for the trip
    '''
    things_todo_response = []
    things_todo_request = requests.get(url=config.EXPEDIA_THINGS_TODO.format(destination_name),
                                       headers={"key": config.EXPEDIA_API_KEY})
    for thing in json.loads(things_todo_request.content)['activities']:
        thing_element = {}
        thing_element['title'] = thing['title']
        thing_element['image'] = 'http' + thing['imageUrl']
        thing_element['categories'] = str(','.join(thing['categories']))
        thing_element['duration'] = thing['duration']
        thing_element['price'] = thing['fromPrice']
        thing_element['rating'] = thing['scoreOutOf5']
        things_todo_response.append(thing_element)

    '''
    get car rentals for the trip
    '''
    pick_date = (datetime.date.today() + datetime.timedelta(days=7)).strftime("%Y-%m-%d")
    return_date = (datetime.date.today() + datetime.timedelta(days=10)).strftime("%Y-%m-%d")
    car_rental_res = []

    car_rentals_requests = requests.get(
        url=config.EXPEDIA_CAR_RENTALS.format(pick_date, return_date, distination_airport_code,
                                              distination_airport_code), headers={"key": config.EXPEDIA_API_KEY})
    car_rentals_requests_json = json.dumps(bf.data(fromstring(car_rentals_requests.content)))
    car_rentals_requests_json = car_rentals_requests_json.replace("{urn:expedia:wsapi:shop:car:v1}", "")
    car_rentals_requests_json = \
        json.loads(car_rentals_requests_json.replace("{urn:expedia:wsapi:shop:car:v1}", ""))['CarSearchResponse'][
            'CarInfoList']['CarInfo']
    for car in car_rentals_requests_json:
        car_ele = {}
        car_ele['SupplierName'] = str(car['SupplierName']['$'])
        car_ele['image'] = '' if 'ThumbnailUrl' not in car else  str(car['ThumbnailUrl']['$'])
        car_ele['CarClass'] = str(car['CarClass']['$'])
        car_ele['CarMakeModel'] = 'N/A' if 'CarMakeModel' not in car else str(car['CarMakeModel']['$'])
        car_ele['CarClass'] = str(car['CarClass']['$'])
        car_ele['Capacity'] = "Adult {0}, Child {1}, Small Luggage {2},Large Luggage {3}".format(
            str(car['Capacity']['AdultCount']['$']), str(car['Capacity']['ChildCount']['$']),
            str(car['Capacity']['SmallLuggageCount']['$']), str(car['Capacity']['LargeLuggageCount']['$']))
        car_ele['Price'] = "Base Rate {0} USD".format(car['Price']['BaseRate']['Value']['$'])
        car_ele['address'] = " {0},{1},{2}".format(str(car['PickupInfo']['Location']['StreetAddress']['$']),
                                                   str(car['PickupInfo']['Location']['City']['$']),
                                                   str(car['PickupInfo']['Location']['Province']['$']))
        car_rental_res.append(car_ele)
    response_dict['trips'] = {
        "CarRentals": car_rental_res,
        "hotels": hotels_list,
        "flights": flights,
        'ThingsToDo': things_todo_response
    }

    return response_dict
