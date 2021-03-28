import random


from django.shortcuts import render, redirect
from django.urls import reverse

from waifu.models import UrlModel
from datetime import datetime


def generate_short_url():  # random url generator
    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    short_url = ''
    for i in range(5):
        char = random.choice(alphabet)
        short_url += char
    return short_url


def short_url_filter(short_url):
    url = UrlModel.objects.get(short_url=short_url)
    return url


def main_url_filter(main_url):
    url = UrlModel.objects.get(main_url=main_url)
    return url


def main_page_url(request):
    if request.method == 'POST':
        url = request.POST.get('main_url').lower()
        custom_url = request.POST.get('custom_url')
        if url[:7] == 'http://' or url[:8] == 'https://':
            split_url = url.split()  # check for space in the end and make url exclusive
            main_url = split_url[0]
        else:
            if not url:  # if nothing submited
                context = {
                    'valid': 'Please, enter URL to convert'
                }
                return render(request, 'main_page.html', context)
            else:  # create url in one style
                split_url = url.split()
                main_url = 'http://' + split_url[0]
        if not UrlModel.objects.filter(main_url=main_url):  # if main url not in db
            time = str(datetime.now())
            if not custom_url:  # if custom url not send - generate random
                short_url = generate_short_url()
                while UrlModel.objects.filter(short_url=short_url):  # if generated url in db - generate new
                    short_url = generate_short_url()
            else:
                if UrlModel.objects.filter(short_url=custom_url):  # if custom url in use
                    context = {
                        'valid': 'Custom URL is already in use'
                    }
                    return render(request, 'main_page.html', context)
                else:
                    short_url = custom_url
            UrlModel.objects.create(main_url=main_url, short_url=short_url, time_add=time, click=0)
            url1 = reverse('redir', args=[short_url])  # create model of url
            dom = request.get_host()
            context = {
                'valid': f'Link generated! Your link: ',
                'link': f'{url1}',
                'host': f'{dom}'
            }
            return render(request, 'main_page.html', context)
        else:  # if send url in db
            model = main_url_filter(main_url)
            short_url = model.short_url
            url1 = reverse('redir', args=[short_url])
            dom = request.get_host()
            context = {
                'valid': f'This URL has already been converted. Link: ',
                'link': f'{url1}',
                'host': f'{dom}'
            }
            return render(request, 'main_page.html', context)
    else:  # if GET
        return render(request, 'main_page.html')


def redirect_to(request, short_url):  # redirect to url and register click in db
    url_model_check = UrlModel.objects.filter(short_url=short_url)
    if url_model_check:
        model = UrlModel.objects.get(short_url=short_url)
        main_url = model.main_url
        model.click += 1
        model.save()
        return redirect(main_url)
    else:
        context = {
            'valid': 'URL not found. Please, try again'
        }
        return render(request, 'main_page.html', context)
