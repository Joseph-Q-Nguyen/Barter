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
from django.http import HttpResponse
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
		results = Item.objects.all().order_by("-date_posted")[offset: offset + POSTS_PER_PAGE]
		if search_query.strip():
			search_keywords = search_query.split()
			# return matches from title or description. Matches are based on any of the words in the search
			results = Item.objects.filter(
				reduce(operator.or_, (Q(title__icontains=k) for k in search_keywords)) 
				|
				reduce(operator.or_, (Q(description__icontains=k) for k in search_keywords))
			).order_by("-date_posted")[offset: offset + POSTS_PER_PAGE]
		
		context={'posts': results}
		check_login(request ,context)
		return render(request, "index.html", context=context)
	check_for_wishlist_update(request)
	search_query = request.GET.get("search_query")
	param_string = get_param_string(request, search_query)
	return redirect(REDIRECT_URL + param_string)


def login_user(request):
	context = {'is_login': True, 'logged_in': False, 'form':LoginForm()}
	if request.method == "POST":
		data = request.POST
		if 'login' in data:
			login_form = LoginForm(data)
			if login_form.is_valid():
				username = data['username']
				password = data['password']
				user = authenticate(request, username=username, password=password)
				login(request, user=user)
				return index(request)
		elif 'register' in data:
			context['form'] = RegisterForm()
			context['is_login'] = False
			return render(request, 'main_app/signin.html', context=context)
		else:
			context['is_login'] = False
			reg_form = RegisterForm(request.POST)
			context['form'] = reg_form
			if reg_form.is_valid():
				fname, lname = data['name'].split(' ')
				uname = data['username']
				email = data['email']
				pwd = data['password']
				user = User.objects.get_or_create(username=uname, email=email, first_name=uname, last_name=lname)[0]
				user.set_password(pwd)
				user.save()
				context['form'] = LoginForm()
				return index(request)
	return render(request, "main_app/signin.html", context=context)

def logout_user(request):
	logout(request)
	return index(request)

def createlisting(request):
	form = ListingForm()
	context = {'form': form}
	check_login(request ,context)
	if context['logged_in'] == True:
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
				user = User.objects.filter(username=request.user)[0]
				image_link=fields['image_link']

				item = Item.objects.get_or_create(user=user, pid=pid, category=category, 
				title=title, date_posted=date_posted, description=description, price=price, image_link=image_link)[0]
				item.save()
				return index(request)

		return render(request, "sell.html", context=context)
	else:
		context = {'form' : LoginForm(),'is_login': True, 'logged_in': False}
		return redirect(REDIRECT_URL + "login", context=context)

def update_listing(request, pid):
	user = User.objects.filter(username=request.user)[0]
	item_to_update = Item.objects.filter(pid=pid, user=user)
	if not item_to_update: # if item does not belong to user, return home page
		return index(request)

	i = item_to_update[0]
	old_vals = {
		'title': i.title,
		'description' : i.description,
		'category': i.category,
		'price' : i.price,
		'image_link' : i.image_link
	}
	form = ListingForm(old_vals)
	context = {'form': form}
	check_login(request ,context)

	if request.method == "POST":
		fields = request.POST
		listing = ListingForm(fields)
		if listing.is_valid():
			category=fields['category']
			title=fields['title']
			price=fields['price']
			description=fields['description']
			image_link=fields['image_link']

			Item.objects.filter(pid=pid, user=user).update(category=category, title=title, description=description, price=price, image_link=image_link)
			return index(request)
	return render(request, "update.html", context=context)


def delete_listing(request, pid):
	user = User.objects.filter(username=request.user)[0]
	item_to_delete = Item.objects.filter(pid=pid, user=user)
	if not item_to_delete: # if item does not belong to user, return home page
		return index(request)
	item_to_delete[0].delete()
	return index(request)
	


def productpage(request, pid):
	check_for_wishlist_update(request)
	
	thisitem = None
	item_list = Item.objects.filter(pid=str(pid))
	if len(item_list) > 0:
		thisitem = item_list[0]
	else:
		return HttpResponse(status=404)
	context = {'thisitem': thisitem}
	check_login(request ,context)

	return render(request, "productpage.html", context)


def user_page(request, id):
	check_for_wishlist_update(request)
	context = {}
	check_login(request, context)
	user = User.objects.filter(id=id)
	if user:
		context['specified_user'] = user[0]
		context['specified_user_items'] = Item.objects.filter(user=user[0]).order_by("-date_posted")
	return render(request, "user_page.html", context)

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


def check_login(request, context):
	if not request.user.is_anonymous:
			context['logged_in'] = True
			context['user'] = request.user
			user = User.objects.filter(username=request.user)[0]
			wishlist = Wishlist.objects.filter(user=user)
			context['wishlist'] = wishlist
			context['wishlist_pids'] = list(map(lambda x : x.item.pid, wishlist))
			context['user_items'] = Item.objects.filter(user=request.user)
	else:
			context['logged_in'] = False

def check_for_wishlist_update(request):
	if request.method == "POST":
		if "add_to_wishlist" in request.POST and "pid" in request.POST:
			add_to_wishlist(request.POST["pid"], User.objects.filter(username=request.user)[0])
		elif "remove_from_wishlist" in request.POST and "pid" in request.POST:
			remove_from_wishlist(request.POST["pid"], User.objects.filter(username=request.user)[0])

def get_param_string(request, search_query):
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
	return param_string