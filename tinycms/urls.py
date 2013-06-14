from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^$', 'tinycms.views.home', name='home'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<hour>\d{2})/(?P<entry_id>\d+)/$', 'tinycms.views.entry_detail', name='entry_detail'),
    url(r'^preview/(?P<entry_id>\d+)/$', 'tinycms.views.preview_entries', name='preview'),

    url(r'^media-upload/$', 'tinycms.views.upload_page', name='upload_page'),
    url(r'^upload/$', 'tinycms.views.upload', name='upload'),

    url(r'^(?P<slugs>[\w\-_/]+)/$', 'tinycms.views.category_detail', name="category_detail"),
)

urlpatterns += staticfiles_urlpatterns()
