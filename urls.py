from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index_view, name='index'),
    url(r'prof/(?P<prof_id>[0-9]+)/$', views.prof_view, name='prof'),
    url(r'group/(?P<group_id>[0-9]+)/$', views.group_view, name='group'),
    url(r'timeslots/$', views.timeslots_view, name='timeslots'),
    url(r'coursemanager/$', views.manage_courses, name='coursemanager'),
    url(r'list_upload/$', views.list_upload, name='listupload'),
]




__author__ = 'dinu'
