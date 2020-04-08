from django.shortcuts import render, redirect
from django.urls import reverse
from django.forms import ValidationError
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegisterForm
from .models import Item
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from functools import reduce
import operator

REDIRECT_URL = "http://localhost:8000/"
POSTS_PER_PAGE = 10

# Create your views here.
def index(request):
	if (request.method == "GET"):
		offset = request.GET.get("offset")
		search_query = request.GET.get("search_query")
		if offset and offset.isdigit():
			offset = int(offset)
		else:
			offset = 0
	
		if type(search_query) is not str:
			search_query = ""
		results = Item.objects.all()[offset: offset + POSTS_PER_PAGE]
		if search_query:
			search_keywords = search_query.split()
			# return matches from title or description. Matches are based on any of the words in the search
			results = Item.objects.filter(
				reduce(operator.or_, (Q(title__icontains=k) for k in search_keywords)) 
				|
				reduce(operator.or_, (Q(description__icontains=k) for k in search_keywords))
			)[offset: offset + POSTS_PER_PAGE]
		
		context={'posts': results}
		if not request.user.is_anonymous:
			context['logged_in'] = True
			context['user'] = request.user
		return render(request, "index.html", context=context)
	else:
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