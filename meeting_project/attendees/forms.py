from django import forms
from .models import Attendee
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class AttendeeForm(forms.ModelForm):
    class Meta:
        model = Attendee
        fields = ['name', 'place', 'job', 'phone', 'num_persons', 'prize']

class StallKeeperLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)