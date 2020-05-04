from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

text_widget = forms.TextInput(attrs={'class':'form-control'})
pwd_widget = forms.PasswordInput(attrs={'class':'form-control'})

class LoginForm(forms.Form):
	username = forms.CharField(required=False, label='Username', widget=text_widget)
	password = forms.CharField(required=False, label='Password', widget=pwd_widget)

	def clean(self):
		data = super().clean()
		if len(data['username']) == 0:
			raise forms.ValidationError("Username field cannot be empty")
		if len(data['password']) == 0:
			raise forms.ValidationError("Password field cannot be empty")
		if authenticate(username=data['username'], password=data['password']) == None:
			raise forms.ValidationError("Incorrect Username/Password")


class RegisterForm(forms.Form):
	name = forms.CharField(label='Full Name', widget=text_widget)
	username = forms.CharField(label='User Name', widget=text_widget)
	email = forms.EmailField(label='Email', widget=text_widget)
	password = forms.CharField(label='Password', widget=pwd_widget)
	confirm_password = forms.CharField(label='Confirm Password', widget=pwd_widget)

	def clean(self):
		data = super().clean()
		uname = data['username']
		email = data['email']
		pwd = data['password']
		c_pwd = data['confirm_password']
		if User.objects.filter(username=uname).exists():
			raise forms.ValidationError("User already exists. Try a different username.")
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError("Email already registered.")
		if email.split('@')[1] != 'sjsu.edu':
			raise forms.ValidationError("Email domain must belong to San Jose State University")
		if pwd != c_pwd:
			raise forms.ValidationError("Passwords do not match.")
		return self.data

class ListingForm(forms.Form):
	FN = 'FN'
	BK = 'BK'
	ED = 'ED'
	DG = 'DG'
	AP = 'AP'
	AC = 'AC'
	SH = 'SH'
	ST = 'ST'

	categories=	[
		(FN, 'Furniture'),
		(BK, 'Book'),
		(ED, 'Electronic Device'),
		(DG, 'Digital Good'),
		(AP, 'Apparel'),
		(SH, 'Shoes'),
		(AC, 'Accessories'),
		(ST, 'College Supply')
	]

	title= forms.CharField(label='Item Name', widget=text_widget)
	category=forms.CharField(label='Category', widget=forms.Select(attrs={'class':'custom-select'}, choices=categories))
	image=forms.CharField(label='Image Link', widget=text_widget)
	price=forms.DecimalField(label='Price', widget=forms.NumberInput(attrs={'class':"form-control"}), min_value=0.01)
	description=forms.CharField(label='Description', widget=forms.Textarea(attrs={'class':'form-control'}))
