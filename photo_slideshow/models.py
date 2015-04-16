from django.db import models
from django.forms import ModelForm


class PhotoMessage(models.Model):
    name = models.CharField(max_length=255, verbose_name="Your name")
    message = models.CharField(max_length=255, verbose_name="Message")
    photo = models.ImageField(upload_to='slideshow', verbose_name="Photo")

    def photo_html(self):
        return u'<img src="%s" style="width: 100px;"/>' % self.photo.url

    photo_html.short_description = 'Photo'
    photo_html.allow_tags = True


class PhotoMessageForm(ModelForm):
    class Meta:
        model = PhotoMessage
        exclude = []
        widgets = {
        }
