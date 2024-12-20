from django.contrib import admin
from .models import *
# Register your models here.

class RegistrationInLine(admin.TabularInline):
    model=Registration
    fields=['user','event']
    extra=0

    def user(self,obj):
        return f'{obj.user.roll_no} - {obj.user.name}'

class EventAdmin(admin.ModelAdmin):
    list_display=['title','date','venue','start_time','organiser']
    inlines=[RegistrationInLine]

admin.site.register(Event,EventAdmin)

class UserRegInLine(admin.TabularInline):
    model=Registration
    fields=['event']
    extra=0

class UserAdmin(admin.ModelAdmin):
    list_display=['username','name']
    inlines=[UserRegInLine]

admin.site.register(User,UserAdmin)
