from django.urls import path
from . import views

urlpatterns = [
    path('scrapper/', views.scrappview, name='scrapper'),
]
