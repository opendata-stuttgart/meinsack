# coding=utf-8
from rest_framework import routers
from django.conf.urls import patterns, include, url

from .views import ZipCodeView

router = routers.DefaultRouter()

urlpatterns = patterns(
    '',
    url(r'^$', ZipCodeView.as_view()),
    url(r'^(?P<zipcode>\d{5})/$', ZipCodeView.as_view()),
)
