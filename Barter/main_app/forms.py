from django import forms

text_widget = forms.TextInput(attrs={'class':'form-control'})
pwd_widget = forms.PasswordInput(attrs={'class':'form-control'})

class LoginForm(forms.Form):
	username = forms.CharField(required=False, label='Username', widget=text_widget)
	password = forms.CharField(required=False, label='Password', widget=pwd_widget)

	# def clean(self):
	# 	data = super().clean()
	# 	if len(data['username']) == 0:
	# 		raise forms.ValidationError("Username field cannot be empty")
	# 	if len(data['password']) == 0:
	# 		raise forms.ValidationError("Password field cannot be empty")

class RegisterForm(forms.Form):
	name = forms.CharField(label='Full Name', widget=text_widget)
	email = forms.EmailField(label='Email', widget=text_widget)
	phone = forms.CharField(label='Phone Number', widget=text_widget)
	password = forms.CharField(label='Password', widget=pwd_widget)
	confirm_password = forms.CharField(label='Confirm Password', widget=pwd_widget)

	def clean(self):
		data = super().clean()
		email = data['email']
		print(email)
		if email.split('@'[1]) != 'sjsu.edu':
			raise ValidationError("Email domain must belong to San Jose State University")
		if password != confirm_password:
			raise ValidationError("Passwords do not match.")
