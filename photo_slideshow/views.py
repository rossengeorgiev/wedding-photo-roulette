from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from photo_slideshow.models import PhotoMessage, PhotoMessageForm
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


def send_photomessage(request):
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
