from django.urls import path
from django_pyp8s.views import IndexView, VersionView, MetricsView


app_name = 'django_pyp8s'
urlpatterns = [

    path("",          IndexView,     name="index"),
    path("version",   VersionView,   name="version"),
    path("metrics",   MetricsView,   name="version"),

]