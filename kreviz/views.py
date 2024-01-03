# kreviz/views.py

from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

from matcher.models import Interest
from account.models import Account

from django.db.models import Count





@login_required
def view_matches(request):
    # call the matches
    matches = Account.find_matches(request.user)
    # render matches in matches.html
    return render(request, "matches.html", {'matches': matches})


def home(request):
    return render(request, 'snippets/home.html')

def index(request):
    return render(request, 'snippets/home.html')

def about(request):
    return render(request, 'core/about.html')

    
