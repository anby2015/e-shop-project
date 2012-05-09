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