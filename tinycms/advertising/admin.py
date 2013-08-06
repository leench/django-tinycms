from django.contrib import admin

from models import Advertising, Media

class MediaAdmin(admin.TabularInline):
    model = Media
    extra = 2

class AdvertisingAdmin(admin.ModelAdmin):
    list_display = ('title', 'adv_title', 'identifier', 'start_date', 'end_date', 'active')
    inlines = [MediaAdmin, ]

admin.site.register(Advertising, AdvertisingAdmin)
