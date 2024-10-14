from django import forms
from .models import Attendee,Person,Profile
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField as FormPhoneNumberField


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES)
    phone = forms.CharField(max_length=15, required=False)
    address = forms.CharField(max_length=255, required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'role','phone','address']


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if User.objects.filter(username=user.username).exists():
            raise forms.ValidationError("A user with this username already exists.")

        if commit:
            user.save()
            profile, created = Profile.objects.update_or_create(
                user=user,
                role=self.cleaned_data['role'],
                phone=self.cleaned_data['phone'],
                address=self.cleaned_data['address']
            )


        else:
            print("form is not committed")

        return user

class AttendeeForm(forms.ModelForm):

    phone = FormPhoneNumberField(required=True, widget=forms.TextInput(attrs={'type': 'tel'}))

    class Meta:
        model = Attendee
        fields = ['name', 'place', 'job', 'gender', 'phone','num_persons', 'email']

    num_persons = forms.IntegerField(min_value=0, label='Number of Persons')

    def clean_num_persons(self):

        num_persons = self.cleaned_data.get('num_persons')


        return num_persons

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'age', 'gender']


class LoginForm(forms.ModelForm):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class AttendeeVerificationForm(forms.ModelForm):
    name_verified = forms.BooleanField(required=False)
    phone_verified = forms.BooleanField(required=False)
    place_verified = forms.BooleanField(required=False)
    job_verified = forms.BooleanField(required=False)
    gender_verified = forms.BooleanField(required=False)
    email_verified = forms.BooleanField(required=False)

    class Meta:
        model = Attendee
        fields = ['name_verified', 'place_verified', 'job_verified', 'gender_verified', 'phone_verified','email_verified']

    def __init__(self, *args, **kwargs):
        super(AttendeeVerificationForm, self).__init__(*args, **kwargs)

class PersonVerificationForm(forms.ModelForm):
    verified = forms.BooleanField(required=False)

    class Meta:
        model = Person
        fields = ['verified']

    def __init__(self, *args, **kwargs):
        super(PersonVerificationForm, self).__init__(*args, **kwargs)
        self.fields['verified'].label = "Person Verified"