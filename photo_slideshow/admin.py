from django.contrib import admin
from photo_slideshow.models import PhotoMessage


class PhotoMessageAdmin(admin.ModelAdmin):
    list_display = ('photo_html', 'name', 'message')
    search_fields = ('name', 'message')

# Register your models here.
admin.site.register(PhotoMessage, PhotoMessageAdmin)
