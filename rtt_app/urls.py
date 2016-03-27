from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.board_list, name='board_list'),
    url(r'^board/(?P<pk>[0-9]+)/$', views.board_detail, name='board_detail'),
    url(r'^board/new/$', views.board_new, name='board_new'),
    url(r'^board/(?P<pk>[0-9]+)/edit/$', views.board_edit, name='board_edit'),
    url(r'^board/(?P<pk>[0-9]+)/publish/$', views.board_publish, name='board_publish'),
    url(r'^board/(?P<pk>[0-9]+)/remove/$', views.board_remove, name='board_remove'),
    url(r'^board/(?P<pk>[0-9]+)/card/new/$', views.card_create, name='card_create'),
    url(r'^board/(?P<pk>[0-9]+)/card/(?P<card_id>[0-9]+)/remove/$', views.card_remove, name='card_remove'),
]