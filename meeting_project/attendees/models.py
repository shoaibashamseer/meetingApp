from django.db import models

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
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)

    def __str__(self):
        return self.name
