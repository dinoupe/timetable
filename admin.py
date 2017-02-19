from django.contrib import admin
from .models import *

admin.site.register(Group)
admin.site.register(Room)
admin.site.register(TimeSlot)
admin.site.register(Prof)
admin.site.register(Course)

# Register your models here.
