from django.shortcuts import render, redirect
from django.urls import reverse
from django.forms import ValidationError
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegisterForm, ListingForm
from .models import Item
from django.contrib.auth.models import User

# Create your views here.
def index(request):
	if (request.method == "GET"):
		offset = request.GET.get("offset")
		if offset and offset.isdigit():
			offset = int(offset)
		else:
			offset = 0
		context={'posts': Item.objects.all()[offset: offset + 10]}
		if not request.user.is_anonymous:
			context['logged_in'] = True
			context['user'] = request.user
		return render(request, "index.html", context=context)
	else:
		offset_string = request.GET.get("offset")
		offset = 0
		if offset_string and offset_string.isdigit():
			offset = int(offset_string)
		if "next" in request.POST:
			offset = offset + 10
		elif "previous" in request.POST:
			offset = offset - 10
		return redirect("http://localhost:8000/?offset=" + str(offset))


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
	return render(request, "sell.html", context=context)