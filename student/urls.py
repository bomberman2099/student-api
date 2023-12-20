from django.urls import path
from . import views

urlpatterns = [
    path('list', views.StudentApiView.as_view(), name='list-student')
]
