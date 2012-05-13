from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from EShop.shop.views import profile, register, requires_login, edit_user_profile, show_profile, send_message,\
    purchase
from django.contrib.auth.views import login, logout
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'EShop.views.home', name='home'),
    # url(r'^EShop/', include('EShop.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/backup/$', 'shop.views.backup'),
    url(r'^admin/statistics/$', 'shop.views.statistics'),
    url(r'^admin/statistics_result', 'shop.views.statistics_result'),
    url(r'^admin/all_statistics', 'shop.views.all_statistics'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'shop.views.index'),
    (r'^accounts/login/$',  login),
    (r'^accounts/logout/$', logout),
    (r'^accounts/profile/$', requires_login(profile)),
    (r'^accounts/profile/(?P<user_id>\d+)$', requires_login(show_profile)),
    (r'^sendmessage/(?P<user_id>\d+)$', requires_login(send_message)),
    (r'^accounts/profile/edit/$', requires_login(edit_user_profile)),
    (r'^accounts/registration/$', register),
    (r'^accounts/profile/purchase/$', requires_login(purchase)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)