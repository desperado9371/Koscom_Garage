from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('algo/',views.algo, name='algo'),
    path('', views.post_list, name='post_list'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)