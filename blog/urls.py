from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # представление поста
    #path(route='', view=views.post_list, name='post_list'), # ПП
    path(route='', view=views.PostListView.as_view(), name='post_list'), # ООП
    path(route='<int:year>/<int:month>/<int:day>/<slug:post>/', view=views.post_detail, name='post_detail'),
]



