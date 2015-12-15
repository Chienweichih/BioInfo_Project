from django.shortcuts import render

API_KEY = "a4a36c45-883f-432e-9dec-5db68f11f767"

def index(request):
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
			context = query(cd['query_text'])
			return render(request, 'bioPortal/query.html', context)
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
	from json2html import json2html
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

def query(query_text):
	context = {'query_text' : query_text}
	return context

def named_entity(named_entity_text):
	context = {'named_entity_text' : named_entity_text}
	return context

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
