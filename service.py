#!/usr/bin/env python
# encoding: utf-8
"""

 @license: Licensed Materials - Property of IBM

 @copyright: (c) Copyright IBM Corporation 2018, 2018. All Rights Reserved.

 @note: Note to U.S. Government Users Restricted Rights: Use, duplication or disclosure restricted by GSA ADP
 Schedule Contract with IBM Corp.

 @author: Sovongsa Ly

 @contact: sly@us.ibm.com
"""

from WatsonAdapter import WatsonNaturalLanguageProcessingAdapter
import WatsonAdapter

def get_recommended_places(input):
    return WatsonNaturalLanguageProcessingAdapter().analyze(input)

def get_recommend_trips(input):
    return WatsonAdapter.get_recommended_trip(input)