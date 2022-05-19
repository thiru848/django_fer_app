from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('faq', views.faq, name='faq'),
    path('signup', views.signup, name='signup'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('forgot', views.forgot, name='forgot'),
    path('callotp', views.callotp, name='callotp'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('verify', views.verify, name='verify'),
    path('profile', views.profile, name='profile'),
    path('reset', views.reset, name='reset'),
    path('music', views.music, name='music'),
    path('report', views.report, name='report'),
    path('update', views.update, name='update'),
    path('photo', views.photo, name='photo'),
]
