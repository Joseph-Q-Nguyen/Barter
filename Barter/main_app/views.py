from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from .models import Item

# Create your views here.
def index(request, offset, limit):
	return render(request, "index.html", context={'posts': Item.objects.all()[offset:limit]})

def login(request):
	form = LoginForm()
	context = {'logged_in': False, 'login_form': form}
	if request.method == "POST":
		lform = LoginForm(request.POST)
		if lform.is_valid():
			print(lform)
			username = lform['username']
			password = lform['password']
			if 'login' in lform:
				print("Logging in..")
			else:
				print("Registering...")
			user = authenticate(request, username=username, password=password)
			context['logged_in'] = user != None
	return render(request, "main_app/signin.html", context=context)