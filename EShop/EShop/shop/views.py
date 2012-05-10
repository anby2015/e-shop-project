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
import os, time
import subprocess
from django.shortcuts import redirect
from django.conf import settings

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
    from django.db import connection
    from django.conf import settings
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