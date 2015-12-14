from django.conf.urls import url

from . import views

urlpatterns = [
	# ex: /bioPortal/
    url(r'^$', views.index, name='index'),
    # ex: /bioPortal/display_all_data/
    url(r'^display_all_data/$', views.display_all_data, name='display_all_data'),
    # ex: /bioPortal/query=Protein/
    url(r'^query=(?P<query_text>[a-zA-Z0-9]+)/$', views.query, name='query'),
    # ex: /bioPortal/abstract=Protein Protein Protein/
    url(r'^abstract=(?P<abstract_text>[a-zA-Z0-9]+)/$', views.named_entity, name='named_entity'),
]
