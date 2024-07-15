from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db import models

class Attendee(models.Model):
    unique_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    job = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    num_persons = models.IntegerField()
    prize = models.CharField(max_length=255, blank=True)
    arrived = models.BooleanField(default=False)
    #qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)
    qr_code = models.CharField(max_length=100,default='6f986337-2964-4dc2-859e-0e9859c35a97')  # Assuming the QR code is a string
    email = models.EmailField(default='shobikunnariyath@gmail.com')

    def __str__(self):
        return self.name


class Stall(models.Model):
    name = models.CharField(max_length=100)
    keeper = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class StallVisit(models.Model):
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    stall = models.ForeignKey(Stall, on_delete=models.CASCADE)
    visit_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.attendee.name} visited {self.stall.name}"