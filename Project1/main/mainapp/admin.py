from django.contrib import admin
from .models import Event
from .models import readingMaterial, classList


# Register your models here.
admin.site.register(Event) #copilot
admin.site.register(readingMaterial)
admin.site.register(classList)