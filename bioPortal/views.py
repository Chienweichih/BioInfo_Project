from django.shortcuts import render

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
	html = ""	
	with open('go_name.data') as go_term:
		for index, line in enumerate(go_term.readlines()):
			html += ("%05d" % index) + " "
			html += "<a href='/bioPortal/query/" + line  + "/' >" + line + "</a><br />"
	context = {'result' : html}
	return render(request, 'bioPortal/display_all_data.html', context)

def query(request, query_text):
	html = ""
	with open('go_term.data') as go_term:
		lines = go_term.readlines()

		for index, line in enumerate(lines):
			if line.startswith('name: ') and line[6:-1] == query_text:
				new_index = index - 1
				while not lines[new_index].startswith('\n'):
					html += lines[new_index] + "<br />"
					new_index += 1
				break

	context = {'result' : html}
	return render(request, 'bioPortal/query.html', context)

def named_entity(named_entity_text):
	html = ""
	with open('go_name.data') as go_term:
		lines = go_term.readlines()
		
		while len(named_entity_text) != 0:
			result_candidate = []
			for line in lines:
				if named_entity_text.startswith(line[:-1]):
					result_candidate.append(line)

			if result_candidate:
				result = max(result_candidate, key=len)[:-1]
				html += "<a href='/bioPortal/query/" + result + "/' >" + result + "</a>"
				named_entity_text = named_entity_text[len(result):]

			next_space = named_entity_text.find(" ")
			if next_space != -1:
				html += named_entity_text[:next_space] + " "
				named_entity_text = named_entity_text[next_space + 1:]
			else:
				html += named_entity_text
				break
	
	context = {'named_entity_text' : html}
	return context
