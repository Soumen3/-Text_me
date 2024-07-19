# context_processors.py
from .models import Site

def site(request):
	site = Site.objects.first()  # replace this with your actual query
	return {'site': site}