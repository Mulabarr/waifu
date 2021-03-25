from random import randint

from django.shortcuts import render, redirect

from waifu.models import UrlModel
from datetime import datetime

HOST = 'http://127.0.0.1:8000/'


def generate_short_url():
    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    shorturl = ''
    for i in range(5):
        ind = randint(0, 62)
        char = alphabet[ind]
        shorturl += char
    return shorturl


def short_url_filter(short_url):
    url = UrlModel.objects.get(short_url=short_url)
    return url


def main_url_filter(main_url):
    url = UrlModel.objects.get(main_url=main_url)
    return url


def main_page_url(request):
    if request.method == 'POST':
        url = request.POST.get('main_url')
        main_url = url.lower()
        if not UrlModel.objects.filter(main_url=main_url):
            time = str(datetime.now())
            short_url = generate_short_url()
            while UrlModel.objects.filter(short_url=short_url) is True:
                short_url = generate_short_url()
            UrlModel.objects.create(main_url=main_url, short_url=short_url, time_add=time, click=0)
            context = {
                'valid': f'Link generated! Your link: ',
                'link': f'{HOST}{short_url}'
            }
            return render(request, 'main_page.html', context)
        else:
            model = main_url_filter(main_url)
            short_url = model.short_url
            context = {
                'valid': f'This URL has already been converted. Link: ',
                'link': f'{HOST}{short_url}'
            }
            return render(request, 'main_page.html', context)
    else:
        return render(request, 'main_page.html')


def redirect_to(request, sh_url):
    urlmodel = short_url_filter(sh_url)
    if urlmodel:
        main_url = urlmodel.main_url
        urlmodel.click += 1
        urlmodel.save()
        return redirect(main_url)
    else:
        context = {
            'valid': 'URL not found. Please, try again'
        }
        return render(request, 'main_page.html', context)
