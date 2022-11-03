from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>', views.question, name='question'),
    path('<int:question_id>/results', views.results, name='results'),
    path('<int:question_id>/vote', views.vote, name='vote'),
    path('redis/<str:key>', views.redis, name='redis'),
    path('redis/<str:key>/<str:value>', views.redis_add, name='redis_add'),
    path('openid', views.openid, name='openid'),
]
