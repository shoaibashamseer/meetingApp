from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Attendee(models.Model):
    unique_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    job = models.CharField(max_length=50, choices=[
        ('plumbing', 'Plumbing'),
        ('electrician', 'Electrician'),
        ('engineer', 'Engineer')])
    gender = models.CharField(max_length=10, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')],
        default='Gender')
    phone = PhoneNumberField(blank=True, null=True)
    num_persons = models.IntegerField(null=False, default=1)
    email = models.EmailField(default='example@gmail.com')
    arrived = models.BooleanField(default=False)


    # verification fields
    name_verified = models.BooleanField(default=False)
    place_verified = models.BooleanField(default=False)
    job_verified = models.BooleanField(default=False)
    gender_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Person(models.Model):
    attendee = models.ForeignKey(Attendee, related_name='persons', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')],
        default='male')
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Profile(models.Model):
    ROLE_CHOICES = (
        ('watchman', 'Watchman'),
        ('stall_keeper', 'Stall Keeper'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='stall_keeper')
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return self.user.username



class StallVisit(models.Model):
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    stall = models.ForeignKey(User, on_delete=models.CASCADE)
    visit_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('attendee', 'stall')

    def __str__(self):
        return f"{self.attendee.name} visited by {self.stall.username} at {self.visit_time}"