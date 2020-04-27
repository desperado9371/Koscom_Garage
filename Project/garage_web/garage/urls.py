from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('backtest/', views.backtest, name='backtest'),
    path('algomaker/', views.algomaker, name='algomaker'),
    path('test/', views.test, name='test'),
    path('', views.home, name='home'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)