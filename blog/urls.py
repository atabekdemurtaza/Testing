from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # представление поста
    path(route='', view=views.post_list, name='post_list'),
    path(route='<int:pk>/', view=views.post_detail, name='post_detail')
]


