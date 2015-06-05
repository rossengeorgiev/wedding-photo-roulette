from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.conf import settings
from photo_slideshow.models import PhotoMessage, PhotoMessageForm
from PIL import Image, ExifTags
import qrcode


def slideshow(request):
    pm = PhotoMessage.objects.last()

    return render(request, 'slideshow.html', {
        'pm': pm,
        })


def slideshow_api(request):
    prev = request.GET.get('prev', None)
    maxid = request.GET.get('max', None)

    pm = PhotoMessage.objects.last()

    random = False
    if maxid is not None and prev is not None:
        maxid = int(maxid)
        prev = int(prev)

        # if previous image is the last
        # return a random image from all of them
        if pm.id == maxid:
            pm = PhotoMessage.objects.exclude(id=prev).order_by('?')[0]
            random = True

        # else we get the next photo message
        else:
            pm = PhotoMessage.objects.filter(id__gt=maxid)[0]

    json = {
        'random':  random,
        'url': pm.photo.url,
        'name': pm.name,
        'message': pm.message,
        'id': pm.id
    }

    return JsonResponse(json)


def thankyou(request):
    return render(request, 'thankyou.html')


def photomessage_upload(request):
    if request.method != 'POST':
        return JsonResponse({})

    form = PhotoMessageForm(request.POST, request.FILES)

    json = {
        'success': False
    }

    if form.is_valid():
        form.save(request)

        # rotate image if necessary
        img = Image.open(form.instance.photo)
        exif = img._getexif()

        if exif:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break

            if orientation in exif:
                if exif[orientation] == 3:
                    img = img.rotate(180, expand=True)
                elif exif[orientation] == 6:
                    img = img.rotate(270, expand=True)
                elif exif[orientation] == 8:
                    img = img.rotate(90, expand=True)

                img.save(settings.BASE_DIR + form.instance.photo.url)
                img.close()

        json['success'] = True
    else:
        if 'photo' in form.errors and form.errors['photo'].as_text().find('required') == -1:
            json['error'] = form.errors['photo'].as_text()
        else:
            json['error'] = "All fields are required :("

    return JsonResponse(json)


def photomessage(request):
    if request.method == 'POST':
        form = PhotoMessageForm(request.POST, request.FILES)

        if form.is_valid():
            # form is valid, we say thanks

            form.save(request)
            return HttpResponseRedirect('/thankyou/')

        # fails to validate, we return to photo message
        # for anther go
    else:
        # new post
        form = PhotoMessageForm()

    return render(request, 'photomessage.html', {
        'form': form,
        })


def generate_qrcode(request):
    image = qrcode.make("http://%s" % request.get_host())
    response = HttpResponse(content_type="image/png")
    image.save(response)
    return response
