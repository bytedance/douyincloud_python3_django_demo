from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('text/antidirt', views.antidirt, name='redis_add'),
    path('get_open_id', views.openid, name='openid'),
]
