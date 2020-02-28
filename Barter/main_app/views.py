from django.shortcuts import render
from django.urls import reverse
from django.forms import ValidationError
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegisterForm
from .models import Item
from django.contrib.auth.models import User

# Create your views here.
def index(request):
	context = {'posts': Item.objects.all()}
	if not request.user.is_anonymous:
		context['logged_in'] = True
		print(request.user)
		context['user'] = request.user
		print(request.user.first_name)
	return render(request, "index.html", context=context)

def login_user(request):
	login_form = LoginForm()
	context = {'is_login': True, 'logged_in': False, 'form': login_form}
	if request.method == "POST":
		data = request.POST
		print(data)
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
				user = User.objects.get_or_create(username=''.join(name.lower().split(' ')), password=pwd, email=email, first_name=uname, last_name=lname)
				return render(request, 'main_app/signin.html', context=context)
			else:
				username = data['username']
				password = data['password']
				print(username, password)
				user = authenticate(request, username=username, password=password)
				if user is None:
					raise ValidationError("Incorrect Username/Password")
				login(request, user=user)
				context['logged_in'] = user != None
				context['user'] = user.first_name
				return render(request, 'index.html', context=context)
	return render(request, "main_app/signin.html", context=context)

def logout_user(request):
	logout(request)
	return render(request, 'index.html', context={'logged_in': False})