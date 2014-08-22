from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'shop.views.home', name='home'),
    url(r'^github_webhooks/$', 'ghwebhookslistener.views.github', name='github-webhooks'),

    url(r'^admin/', include(admin.site.urls)),
)