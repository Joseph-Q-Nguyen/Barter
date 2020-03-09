from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from .models import Item

# Create your views here.
def index(request):
	if (request.method == "GET"):
		offset = request.GET.get("offset")
		if offset and offset.isdigit():
			offset = int(offset)
		else:
			offset = 0
		return render(request, "index.html", context={'posts': Item.objects.all()[offset: offset + 10]})
	else:
		offset_string = request.GET.get("offset")
		offset = 0
		if offset_string and offset_string.isdigit():
			offset = int(offset_string)
			if "next" in request.POST:
				offset = offset + 10
			else:
				offset = offset - 10
		return redirect("http://localhost:8000/?offset=" + str(offset))

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