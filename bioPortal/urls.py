from django.conf.urls import url

from . import views

urlpatterns = [
	# ex: /bioPortal/
    url(r'^$', views.index, name='index'),
    # ex: /bioPortal/display_all_data/
    url(r'^display_all_data/$', views.display_all_data, name='display_all_data'),
]
