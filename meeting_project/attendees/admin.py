from django.contrib import admin
from .models import Attendee,StallVisit,Person,Profile

class PersonInline(admin.TabularInline):
    model = Person
    extra = 0

class AttendeesAdmin(admin.ModelAdmin):
    list_display = ('name', 'place', 'unique_id', 'arrived','phone','num_persons')
    search_fields = ('name', 'email', 'unique_id')
    list_filter = ('arrived',)
    inlines = [PersonInline]

class StallVisitAdmin(admin.ModelAdmin):
    list_display = ('attendee', 'stall', 'visit_time')
    search_fields = ('attendee__name', 'stall__name')
    list_filter = ('visit_time',)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone', 'address')
    search_fields = ('user__username', 'role')

admin.site.register(Attendee, AttendeesAdmin)
admin.site.register(StallVisit, StallVisitAdmin)
#admin.site.register(Stall ,StallAdmin )
admin.site.register(Profile, ProfileAdmin)