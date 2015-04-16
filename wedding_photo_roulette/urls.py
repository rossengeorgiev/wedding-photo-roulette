from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wedding_photo_roulette.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    # photo_slideshow views
    url(r'^$', 'photo_slideshow.views.send_photomessage', name='post'),
    url(r'^thankyou/$', 'photo_slideshow.views.thankyou', name='thankyou'),
    url(r'^slideshow/$', 'photo_slideshow.views.slideshow', name='home'),
    url(r'^slideshow/api$', 'photo_slideshow.views.slideshow_api', name='slideshow_api'),
    url(r'^slideshow/qrcode.png$', 'photo_slideshow.views.generate_qrcode', name='qrcode'),
)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
