from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import PassMan


# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)
			
	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def __init__(self, *args, **kwargs):
		super(UserCreationForm, self).__init__(*args, **kwargs)

		for fieldname in ['username', 'password1', 'password2']:
			self.fields[fieldname].help_text = None

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class LoginUserForm(AuthenticationForm):
	def __init__(self, *args, **kwargs):
		super(UserCreationForm, self).__init__(*args, **kwargs)

		for fieldname in ['username', 'password']:
			self.fields[fieldname].help_text = None
   
class PassManForm(forms.ModelForm):
    
    class Meta:
        model = PassMan
        exclude=('user',)