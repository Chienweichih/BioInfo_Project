from django.shortcuts import render
from models import Excuse

def home(request):
    excuse = Excuse.objects.all().order_by('?')[0]
    return render(request, "index.html", {'excuse': excuse})
