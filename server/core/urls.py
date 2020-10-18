from django.urls import path

from core.views import main_page, load

urlpatterns = [
    path('', main_page, name='main_page'),
    path('load/', load, name='load'),
]
