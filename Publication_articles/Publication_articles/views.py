from django.shortcuts import render
from django.http import HttpResponse
# from .models import conference

# Create your views here.
def index(request):
    # conferences = conference.objects.all()
    return render(request,'login/index.html')
