from django.conf.urls import url, include
from . import views
from .models import PredictData
from rest_framework import routers, serializers, viewsets
from .views import index


urlpatterns = [
url(r'^$', index.as_view(), name='index'),
]
