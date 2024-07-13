from django.contrib import admin
from .models import Attendee,Stall,StallVisit
# Register your models here.
class AttendeesAdmin(admin.ModelAdmin):
    list_display = ('name', 'unique_id')

class StallAdmin(admin.ModelAdmin):
    list_display = ('name','keeper')

class StallVisitAdmin(admin.ModelAdmin):
    list_display = ('attendee', 'stall')

admin.site.register(Attendee, AttendeesAdmin)
admin.site.register(StallVisit, StallVisitAdmin)
admin.site.register(Stall ,StallAdmin )