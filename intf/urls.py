from django.conf.urls import url
from django.urls import include
from . import views

urlpatterns = [
    url('asset/',views.asset),
]