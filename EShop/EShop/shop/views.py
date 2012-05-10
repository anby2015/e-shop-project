# -*- coding:utf8 -*-
from django.shortcuts import render_to_response, redirect
from models import Product, Category
from django.template import RequestContext
from shop.models import Banner,Deal
from random import choice
import os, time
from datetime import datetime
import subprocess
from django.conf import settings
from EShop.shop.models import SubCategory
from django.db.models.aggregates import Sum
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils.safestring import mark_safe

def banner():
    banner = Banner.objects.all()
    if banner:
        banner = choice(banner)
        banner.views += 1
        banner.save()
    return banner

def index(request):
    products_list = Product.objects.all()
    response = render_to_response('eshop/list.html',
            {'products_list': products_list, 'banner':banner()},
        context_instance=RequestContext(request))
    response.set_cookie('LANGUAGE_COOKIE_NAME', 'ru')
    request.session["django_language"]="ru"
    return response

def common(request):
    category_list = Category.objects.all().order_by('name')
    return {
        'category_list': category_list,
        }

def do_mysql_backup(conf,outfile):
    args = []
    if conf['user']:
        args += ["--user=%s" % conf['user']]
    if conf['passwd']:
        args += ["--password=%s" % conf['passwd']]
    if conf['host']:
        args += ["--host=%s" % conf['host']]
    if conf['port']:
        args += ["--port=%s" % conf['port']]
    args += [conf['db']]
    os.system('mysqldump %s > %s' % (' '.join(args), outfile))

def do_postgresql_backup(conf,outfile):
    args = ["pg_dump"]
    if conf['user']:
        args += ["--username=%s" % conf['user']]
    if conf['host']:
        args += ["--host=%s" % conf['host']]
    if conf['port']:
        args += ["--port=%s" % conf['port']]
    args += ["--file=%s" % outfile]
    if conf['db']:
        args += [conf['db']]
    subprocess.call(args)

def backup(request):
    conf = {}
    database = settings.DATABASES['default']
    conf['engine'] = database['ENGINE']
    conf['db'] = database['NAME']
    conf['user'] = database['USER']
    conf['passwd'] = database['PASSWORD']
    conf['host'] = database['HOST']
    conf['port'] = database['PORT']
    backup_dir = 'backups'
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    outfile = os.path.join(backup_dir,"backup_%s.sql" % time.strftime('%y%m%d%S'))
    if conf['engine'] == 'mysql':
        do_mysql_backup(conf,outfile)
    elif conf['engine'] in ('django.db.backends.postgresql_psycopg2', 'postgresql'):
        do_postgresql_backup(conf,outfile)
    return redirect('/admin/')

def page_number(prefix,page):
    pages = []
    for i in page.paginator.page_range:
        if i == '.':
            pages.append(u'...')
        elif i == page.number:
            pages.append(mark_safe(u'<span class="this-page">%d</span> ' % i))
        else:
            pages.append(mark_safe(u'<a href="%s?p=%s"%s>%d</a> ' % (prefix,i, (i == page.paginator.num_pages-1 and ' class="end"' or ''), i)))
    return pages

def statistics(request):
    if request.method == 'POST':
        if request.POST.get("_search",None):
            date0 = request.POST.get("date_0",None)
            date1 = request.POST.get("date_1",None)
            error0 = None
            error1 = None
            t0 = date0.split('-')
            t1 = date1.split('-') 
            if len(t0) != 3:
                error0 = True
            else:
                try:
                    date0 = datetime(int(t0[0]),int(t0[1]),int(t0[2]))
                except ValueError:
                    error0 = True
            if len(t1) != 3:
                error1 = True
            else:
                try:
                    date1 = datetime(int(t1[0]),int(t1[1]),int(t1[2]))
                except ValueError:
                    error1 = True
            if error0 or error1:
                return render_to_response('admin/statistics.html',{'error0':error0,'error1':error1}, context_instance=RequestContext(request))
            else:
                deals = Deal.objects.filter(date__gte=date0).filter(date__lte=date1)
                added = deals.filter(action='A')
                sold = deals.filter(action='S')
                subs = SubCategory.objects.all()
                deal_list = []
                for sub in subs:
                    add = added.filter(product__category=sub).aggregate(Sum('num'))['num__sum']
                    sl = sold.filter(product__category=sub).aggregate(Sum('num'))['num__sum']
                    if not add:
                        add = 0
                    if not sl:
                        sl = 0
                    deal_list.append((sub.name,add,sl))
                paginator = Paginator(deal_list, 25)
                request.session["paginator"] = paginator
                deals = paginator.page(1)
                deals.page_num = 1
                pages = page_number('/admin/statistics_result',deals)
                return render_to_response('admin/statistics_result.html',{'deal_list':deals,'paginator_require':len(pages)>1,
                                                                          'pages':pages}, context_instance=RequestContext(request))
        else:
            return redirect('/admin/all_statistics')
    else:
        return render_to_response('admin/statistics.html',{}, context_instance=RequestContext(request))
    
def statistics_result(request):
    paginator = request.session.get("paginator",None)
    if paginator:
        p = request.GET.get('p',1)
        try:
            deals = paginator.page(p)
        except PageNotAnInteger:
            deals = paginator.page(1)
        except EmptyPage:
            deals = paginator.page(paginator.num_pages)
        pages = page_number('/admin/statistics_result',deals)
        return render_to_response('admin/statistics_result.html',{'deal_list':deals,'paginator_require':len(pages)>1,
                                                                  'pages':pages}, context_instance=RequestContext(request))
    else:
        return render_to_response('admin/statistics_result.html',{}, context_instance=RequestContext(request))
    
def all_statistics(request):
    deal_list = Deal.objects.all()
    paginator = Paginator(deal_list, 25)
    p = request.GET.get('p',1)
    try:
        deals = paginator.page(p)
    except PageNotAnInteger:
        deals = paginator.page(1)
    except EmptyPage:
        deals = paginator.page(paginator.num_pages)
    pages = page_number('/admin/all_statistics',deals)
    return render_to_response('admin/all_statistics.html',{'deal_list':deals,'paginator_require':len(pages)>1,
                                                              'pages':pages}, context_instance=RequestContext(request))