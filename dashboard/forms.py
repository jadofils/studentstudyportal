from django.forms import widgets
from django import forms
from django.contrib.auth.forms import UserCreationForm
from . models import *
from .models import Todo
class  NotesForm(forms.ModelForm):
      class Meta:
            model=Notes
            fields=['title','description']


class DateInput(forms.DateInput):
      input_type='date'


from django import forms
from .models import Homework

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ['subject', 'title', 'description', 'due', 'is_finished']  # Corrected 'is_finised' to 'is_finished'

class DashboardForm(forms.Form):
    text=forms.CharField(max_length=100,label="Enter Search Help?")

class TodoForm(forms.ModelForm):
     class Meta:
          model=Todo
          fields=['title','day','time','place','is_finished']


class ConversionForm(forms.Form):
    CHOICES = [
    ('length', 'Length'),
    ('mass', 'Mass')
   
]

    measurement = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

class ConversionLengthForm(forms.Form):
     CHOICES=[('yard','Yard'),('foot','Foot')]
     input=forms.ChoiceField(required=False,label=False,widget=forms.TextInput(
     attrs={'type':'number','placeholder':'Enter The Number'}
     ))

     measure1=forms.CharField(
          label='',widget=forms.Select(choices=CHOICES)
     )  

     measure2=forms.CharField(
          label='',widget=forms.Select(choices=CHOICES)
     ) 


class ConversionMassForm(forms.Form):
     CHOICES=[('pound','Pound'),('kilogram','Kilogram')]
     input=forms.ChoiceField(required=False,label=False,widget=forms.TextInput(
     attrs={'type':'number','placeholder':'Enter The Number'}
     ))

     measure1=forms.CharField(
          label='',widget=forms.Select(choices=CHOICES)
     )  

     measure2=forms.CharField(
          label='',widget=forms.Select(choices=CHOICES)
     ) 

class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'email']  # Include fields you want in the form

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2:
            # Check if passwords match
            if password1 != password2:
                raise forms.ValidationError("Passwords do not match")

            # Check password length
            if len(password1) < 5:
                raise forms.ValidationError("Password must be at least 5 characters long")

            # Check for uppercase letter
            if not any(char.isupper() for char in password1):
                raise forms.ValidationError("Password must contain at least one uppercase letter")

            # Check for number
            if not any(char.isdigit() for char in password1):
                raise forms.ValidationError("Password must contain at least one number")

            # Check for special character
            if not any(char in "!@#$%^&*()_+-=~`[]{}|;:,.<>?/" for char in password1):
                raise forms.ValidationError("Password must contain at least one special character")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.set_password(self.cleaned_data['password1'])
            user.save()
        return user
