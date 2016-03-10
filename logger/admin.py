from django.contrib import admin
from logger.models import PageLoad, MouseClick, Tracker, TrackedUser

# Register your models here.
admin.site.register(Tracker)
admin.site.register(PageLoad)
admin.site.register(MouseClick)
admin.site.register(TrackedUser)
