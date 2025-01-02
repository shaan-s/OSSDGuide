from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('explore', views.explore, name='explore'),
    path("course/<str:code>/",views.course_page, name="course_page"),
    path('contact', views.contact, name='contact')
]
