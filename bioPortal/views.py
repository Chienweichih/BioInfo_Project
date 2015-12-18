from django.shortcuts import render

import urllib2
import json
from json2html import *

REST_URL = "http://data.bioontology.org"
API_KEY = "a4a36c45-883f-432e-9dec-5db68f11f767"

def index(request):
	from django.http import HttpResponseRedirect
	from .forms import QueryForm
	from .forms import NamedEntityForm

	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form_query = QueryForm(request.POST)
		form_named_entity = NamedEntityForm(request.POST)
		# check whether it's valid:
		if form_query.is_valid():
			cd = form_query.cleaned_data
			query_text = cd['query_text']
			return HttpResponseRedirect('/query/%s' % query_text)
		elif form_named_entity.is_valid():
			cd = form_named_entity.cleaned_data
			context = named_entity(cd['named_entity_text'])
			return render(request, 'bioPortal/named_entity.html', context)

	# if a GET (or any other method) we'll create a blank form
	else:
		form_query = QueryForm()
		form_named_entity = NamedEntityForm()

	context = {'form_named_entity' : form_named_entity, 'form_query' : form_query}
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
	#ncbo_sparql
	"""search_result = ncbo_sparql(query_string, API_KEY, sparql_service)
	html = json2html.convert(json = search_result)
	context = {'html' : html}
	return render(request, 'bioPortal/display_all_data.html', context)"""

	return render(request, 'bioPortal/display_all_data_preparation.html')

def query(request, query_text):
	search_result = ncbo_rest(REST_URL + "/search?q=" + query_text, API_KEY)
	
	html = "Query : " + query_text + "<br />"
	if search_result == "ERROR!!" or json.loads(search_result).get('pageCount') == 0:
		html += query_text + " not found!!"
	else:
		html += json2html.convert(json = search_result)
	context = {'result' : html}
	return render(request, 'bioPortal/query.html', context)

def named_entity(named_entity_text):
	named_entity_list = named_entity_text.split()
	result = ""
	for word in named_entity_list:
		test = ncbo_rest(REST_URL + "/search?q=" + word, API_KEY)
		if test == "ERROR!!" or json.loads(test).get('pageCount') == 0:
			result += word + " "		
		else:
			result += "<a href='/bioPortal/query/" + word + "/' >" + word + "</a> "
	context = {'named_entity_text' : result}
	return context

def ncbo_sparql(q,apikey,epr,f='application/json'):
	""" Simple Python script to query "http://sparql.bioontology.org/sparql/"
		No extra libraries required.
	"""
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

def ncbo_rest(url, apikey):
	try:
		opener = urllib2.build_opener()
		opener.addheaders = [('Authorization', 'apikey token=' + apikey)]
		return opener.open(url).read()
	except Exception as e:
		return "ERROR!!"
