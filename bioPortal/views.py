from django.shortcuts import render

from json2html import *

API_KEY = "a4a36c45-883f-432e-9dec-5db68f11f767"

def index(request):
	context = {}
	return render(request, 'bioPortal/index.html', context)

def display_all_data(request):
	sparql_service = "http://sparql.bioontology.org/sparql/"

	#Some sample query.
	query_string = """ 
PREFIX omv: <http://omv.ontoware.org/2005/05/ontology#>

SELECT ?ont ?name ?acr
WHERE { ?ont a omv:Ontology;
	         omv:acronym ?acr;
	         omv:name ?name .
} 
"""
	#search_result = get_json(query_string, API_KEY, sparql_service)
	#html = json2html.convert(json = search_result)
	#context = {'html' : html}
	#return render(request, 'bioPortal/display_all_data.html', context)

	return render(request, 'bioPortal/display_all_data_preparation.html')

def query(request, query_text):
	context = {'query_text' : query_text}
	return render(request, 'bioPortal/query.html', context)

def named_entity(request, abstract_text):
	context = {'abstract_text' : abstract_text}
	return render(request, 'bioPortal/named_entity.html', context)

def get_json(q,apikey,epr,f='application/json'):
	""" Simple Python script to query "http://sparql.bioontology.org/sparql/"
		No extra libraries required.
	"""
	import urllib2
	import urllib
	import traceback
	import sys
 
	"""Function that uses urllib/urllib2 to issue a SPARQL query.
	   By default it requests json as data format for the SPARQL resultset"""

	try:
	    params = {'query': q, 'apikey': apikey}
	    params = urllib.urlencode(params)
	    opener = urllib2.build_opener(urllib2.HTTPHandler)
	    request = urllib2.Request(epr+'?'+params)
	    request.add_header('Accept', f)
	    request.get_method = lambda: 'GET'
	    url = opener.open(request)
	    return url.read()
	except Exception as e:
	    traceback.print_exc(file=sys.stdout)
	    raise e
