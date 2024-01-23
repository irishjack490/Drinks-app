import os
import uuid
import boto3
from django.shortcuts import render, redirect,  get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ShoppingGuide
import requests
# Variables

api = os.environ['APIKEY']
random_10 = '/randomselection.php'
random = '/random.php'
popular_10 = '/popular.php'
latest = '/latest.php'
search = '/search.php?s=' #{Drink Name}
letter_search = '/search.php?f=' #{Drink first letter}
ingredient_search = '/search.php?i=' #{ingredient name}
drink_id = '/lookup.php?i=' #{Lookup by ID for SHOW page}
ingredient_id = '/lookup.php?iid=' #{Lookup ingredient by ID}

# Create views here.

def home(request):
    url = f"https://www.thecocktaildb.com/api/json/v2/{api}{popular_10}"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()

    drinks = filter(lambda drink: drink, response['drinks'])
    return render(request, 'home.html', {'response': response, 'api': api, 'drink_id': drink_id, 'drinks': drinks})


def random_index(request):
    url = f"https://www.thecocktaildb.com/api/json/v2/{api}{random_10}"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()
    drinks = filter(lambda drink: drink, response['drinks'])
    return render(request, 'random.html', {'response': response, 'api': api, 'drink_id': drink_id, 'drinks': drinks})


def about(request):
    return render(request, 'about.html', )


def drinks_index(request):
    url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s=margarita"
    payload = {}
    headers = {}
    response = requests.get(url, headers=headers, data=payload)
    drinks = response.json()['drinks']
    return render(request, 'index.html', {'drinks':drinks})

@login_required
def show_page(request, id_drink):
    ing_arr = []
    url = f'https://www.thecocktaildb.com/api/json/v2/{api}{drink_id}{id_drink}'
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()
    drinks = filter(lambda drink: drink, response['drinks'])
    return render(request, 'show.html', {'response': response, 'api': api, 'drinks': drinks})


# Shopping list Views

class ShoppingGuideCreate(LoginRequiredMixin, CreateView):
    model = ShoppingGuide
    fields = '__all__'
    
class ShoppingGuideList(ListView):
    model = ShoppingGuide

class ShoppingGuideDetail(LoginRequiredMixin, DetailView):
    model = ShoppingGuide

class ShoppingGuideUpdate(LoginRequiredMixin, UpdateView):
    model = ShoppingGuide
    #Change this!
    fields = ['name', 'color']

class ShoppingGuideDelete(LoginRequiredMixin, DeleteView):
    model = ShoppingGuide
    success_url = 'shopping_guide/'

    
def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
    if form.is_valid():
        # Save the user to the db
        user = form.save()
        # Automatically log in the new user
        login(request, user)
        return redirect('index')
    else:
        error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup template
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)