from django.shortcuts import render
from models import Excuse

import urllib2
import json
from json2html import *

REST_URL = "http://data.bioontology.org"
API_KEY = "a4a36c45-883f-432e-9dec-5db68f11f767"

def get_json(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('Authorization', 'apikey token=' + API_KEY)]
    return json.loads(opener.open(url).read())

def home(request):
    term = "protein"
    search_result = get_json(REST_URL + "/search?q=" + term)["collection"]
    html = ""
    for result in search_result:
        html += json2html.convert(json = result)
    return render(request, "index.html", {'result': html})
