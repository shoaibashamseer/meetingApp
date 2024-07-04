from django.contrib import admin
from .models import Attendee

# Register your models here.
class AttendeesAdmin(admin.ModelAdmin):
    list_display = ('name', 'unique_id')

admin.site.register(Attendee, AttendeesAdmin)