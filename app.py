#!/usr/bin/env python
# encoding: utf-8
"""
 @contact: sovongsa.ly@gmail.com
"""

from flask import Flask
from flask_restplus import Api
from Controller import ns_sta

app = Flask(__name__)
api = Api(app, version='1.0', title='Homeaway Hackathon',
          description='Homeaway Hackathon'
          )

api.add_namespace(ns_sta,path="/sta")


app.run(port=5050)
