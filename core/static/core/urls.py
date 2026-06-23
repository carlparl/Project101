from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('safaris/', views.tours_list, name='tours_list'),
    path('safaris/<int:tour_id>/', views.tour_detail, name='tour_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]