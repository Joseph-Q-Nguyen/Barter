from django import forms

class LoginForm(forms.Form):
	username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class':'form-control'}))
	password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))

	# def clean(self):
	# 	data = super().clean()
	# 	if len(data['username']) == 0:
	# 		raise forms.ValidationError("Username field cannot be empty")
	# 	if len(data['password']) == 0:
	# 		raise forms.ValidationError("Password field cannot be empty")
