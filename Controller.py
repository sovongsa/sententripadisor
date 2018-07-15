#!/usr/bin/env python
# encoding: utf-8
"""

 @contact: sovongsa.ly@gmail.com
"""
from flask import Flask, request, abort, jsonify, make_response
from flask_restplus import Namespace, Resource, fields, abort, marshal, reqparse
import service

app = Flask(__name__)
ns_sta = Namespace('Sentiment Trip Advisor', description='Sentiment Trip Advisor')

recommend_trips = ns_sta.model('recommend_trips', {
    "current_lat": fields.String(required=True),
    "current_lng": fields.String(required=True),
    "destination_lat": fields.String(required=True),
    "destination_lng": fields.String(required=True),
    "destination_name":fields.String(required=True)
})


recommend_place_model = ns_sta.model('ns_sta_recommendedplace', {
    "input": fields.String(required=True),
    "current_lat": fields.String(required=True),
    "current_lng":fields.String(required=True)
})


@ns_sta.route('/v1/place')
class RecommendedPlace(Resource):
    @ns_sta.expect(recommend_place_model,validate=True)
    def post(selfs):
        data = request.get_json()
        return service.get_recommended_places(data)

@ns_sta.route('/v1/trips')
class RecommendTrip(Resource):
    @ns_sta.expect(recommend_trips,validate=True)
    def post(selfs):
        data = request.get_json()
        return service.get_recommend_trips(data)

