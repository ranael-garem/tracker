from django.contrib import admin
from logger.models import (PageLoad, MouseClick, Page,
                           Tracker, TrackedUser, Session)


class PageLoadInline(admin.TabularInline):
    model = PageLoad


class MouseClickInline(admin.TabularInline):
    model = MouseClick


class PageAdmin(admin.ModelAdmin):
    model = Page
    inlines = PageLoadInline, MouseClickInline
# Register your models here.
admin.site.register(Tracker)
admin.site.register(PageLoad)
admin.site.register(Page, PageAdmin)
admin.site.register(MouseClick)
admin.site.register(TrackedUser)
admin.site.register(Session)
