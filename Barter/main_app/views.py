from django.shortcuts import render, redirect
from django.urls import reverse
from django.forms import ValidationError
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegisterForm, ListingForm
from .models import Item, Wishlist
from django.contrib.auth.models import User
from datetime import date
import uuid
from django.contrib import messages
from django.db.models import Q
from functools import reduce
import operator

REDIRECT_URL = "http://localhost:8000/"
POSTS_PER_PAGE = 10

# Create your views here.
def index(request):
	if request.method == "GET":
		offset = request.GET.get("offset")
		search_query = request.GET.get("search_query")
		if offset and offset.isdigit():
			offset = int(offset)
		else:
			offset = 0
	
		if type(search_query) is not str:
			search_query = ""
		results = Item.objects.all()[offset: offset + POSTS_PER_PAGE]
		if search_query.strip():
			search_keywords = search_query.split()
			# return matches from title or description. Matches are based on any of the words in the search
			results = Item.objects.filter(
				reduce(operator.or_, (Q(title__icontains=k) for k in search_keywords)) 
				|
				reduce(operator.or_, (Q(description__icontains=k) for k in search_keywords))
			)[offset: offset + POSTS_PER_PAGE]
		
		context={'posts': results}
		check_login(request ,context)
		return render(request, "index.html", context=context)
	elif request.method == "POST":
		if "add_to_wishlist" in request.POST and "pid" in request.POST:
			add_to_wishlist(request.POST["pid"], User.objects.filter(username=request.user)[0])
		elif "remove_from_wishlist" in request.POST and "pid" in request.POST:
			remove_from_wishlist(request.POST["pid"], User.objects.filter(username=request.user)[0])
		search_query = request.GET.get("search_query")
		offset_string = ""
		offset = 0
		query_params = []
		if "search_query" in request.POST:
			search_query = request.POST['search_query']
		else:
			offset_string = request.GET.get("offset")
			if offset_string and offset_string.isdigit():
				offset = int(offset_string)
			if "next" in request.POST:
				offset = offset + POSTS_PER_PAGE
			elif "previous" in request.POST:
				offset = offset - POSTS_PER_PAGE
			offset_string = "offset=" + str(offset)
		if type(offset_string) is not str:
			offset_string = ""
		if type(search_query) is not str:
			search_query = ""
		if search_query:
			search_query = "search_query=" + search_query
		
		search_query = search_query.replace(" ", "+") #replace spaces with a plus sign so theyu can go on url
		query_params.append(search_query)
		query_params.append(offset_string)

		param_string = "?"
		for param in query_params:
			if param:
				param_string = param_string + param + "&"
		param_string = param_string[0:-1] # get rid of last '&'

		return redirect(REDIRECT_URL + param_string)


def login_user(request):
	login_form = LoginForm()
	context = {'is_login': True, 'logged_in': False, 'form': login_form}
	if request.method == "POST":
		data = request.POST
		login_form = LoginForm(data)
		if login_form.is_valid():
			if 'register' in data:
				register_form = RegisterForm()
				context['is_login'] = False
				context['form'] = register_form
				return render(request, 'main_app/signin.html', context=context)
			elif 'sign_up' in data:
				name = data['name']
				uname, lname = name.split(' ')
				email = data['email']
				pwd = data['password']
				user = User.objects.get_or_create(username=''.join(name.lower().split(' ')), email=email, first_name=uname, last_name=lname)[0]
				user.set_password(pwd)
				user.save()
				return render(request, 'main_app/signin.html', context=context)
			else:
				username = data['username']
				password = data['password']
				user = authenticate(request, username=username, password=password)
				if user is None:
					raise ValidationError("Incorrect Username/Password")
				login(request, user=user)
				# context['logged_in'] = user != None
				# context['user'] = user.first_name
				return index(request)
	return render(request, "main_app/signin.html", context=context)

def logout_user(request):
	logout(request)
	return index(request)

def createlisting(request):
	form = ListingForm()
	context = {'form': form}
	check_login(request ,context)
	if request.method == "POST":
		fields = request.POST
		listing = ListingForm(fields)
		if listing.is_valid():
			pid=uuid.uuid4()
			category=fields['category']
			title=fields['title']
			price=fields['price']
			description=fields['description']
			date_posted=date.today()

			item = Item.objects.get_or_create(pid=pid, category=category, title=title, date_posted=date_posted, description=description, price=price)[0]
			item.save()
			return index(request)
	return render(request, "sell.html", context=context)

def productpage(request, pid):
	if request.method == "POST":
		if "add_to_wishlist" in request.POST and "pid" in request.POST:
			add_to_wishlist(request.POST["pid"], User.objects.filter(username=request.user)[0])
		elif "remove_from_wishlist" in request.POST and "pid" in request.POST:
			remove_from_wishlist(request.POST["pid"], User.objects.filter(username=request.user)[0])
	
	thisitem = None
	item_list = Item.objects.filter(pid=str(pid))
	if len(item_list) > 0:
		thisitem = item_list[0]
	else:
		thisitem = None
	context = {'thisitem': thisitem}
	check_login(request ,context)

	return render(request, "productpage.html", context)

# HELPER FUNCTIONS

def add_to_wishlist(pid, user):
	item = Item.objects.filter(pid=str(pid))[0]
	wishlist_item = Wishlist.objects.filter(item=item, user=user)
	if not wishlist_item:
		Wishlist.objects.create(item=item, user=user)

def remove_from_wishlist(pid, user):
	item = Item.objects.filter(pid=str(pid))[0]
	print(item.title)
	wishlist_item = Wishlist.objects.filter(item=item, user=user)
	if wishlist_item:
		wishlist_item[0].delete()


def check_login(request ,context):
	if not request.user.is_anonymous:
			context['logged_in'] = True
			context['user'] = request.user
			user = User.objects.filter(username=request.user)[0]
			wishlist = Wishlist.objects.filter(user=user)
			context['wishlist'] = wishlist
			context['wishlist_names'] = list(map(lambda x : x.item.title, wishlist))