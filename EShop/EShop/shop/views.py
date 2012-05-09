from django.shortcuts import render_to_response
from models import Product, Category
from django.template import RequestContext
from shop.models import Banner
from random import choice

def index(request):
    products_list = Product.objects.all()
    response = render_to_response('eshop/list.html',
            {'products_list': products_list},
        context_instance=RequestContext(request))
    response.set_cookie('LANGUAGE_COOKIE_NAME', 'ru')
    request.session["django_language"]="ru"
    return response

def common(request):
    category_list = Category.objects.all().order_by('name')
    banner = Banner.objects.all()
    if banner:
        banner = choice(banner)
        banner.views += 1
        banner.save()
    return {
        'category_list': category_list,
        'banner': banner,
        }