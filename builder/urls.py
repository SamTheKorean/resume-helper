from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('resume/', views.resume_input, name='resume_input'),
    path('generate_resume/<int:pk>/', views.generate_resume, name='generate_resume'),
]