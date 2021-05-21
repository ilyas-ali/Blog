from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register,name='register'),
    path('lin/', views.lin,name='lin'),
    path('index/', views.index,name='index'),
    path('log/', views.log,name='log'),
    path('create/', views.create,name='create'),
    path('search/', views.search,name='search'),
]