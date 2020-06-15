from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('algomaker/', views.algomaker, name='algomaker'),
    path('test/', views.test, name='test'),
    path('mypage/', views.mypage, name='mypage'),
    path('loading/', views.loading, name='loading'),
    path('intro/', views.intro, name='intro'),
    path('ready/', views.ready, name='ready'),
    path('', views.home, name='home'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)