from django.urls import path
from . import views
from . import feeds

app_name = 'blog'

urlpatterns = [
    # представление поста
    path(route='', view=views.post_list, name='post_list'), # ПП
    #path(route='', view=views.PostListView.as_view(), name='post_list'), # ООП
    path(route='<int:year>/<int:month>/<int:day>/<slug:post>/', view=views.post_detail, name='post_detail'),
    path(route='<int:post_id>/share/', view=views.post_share, name='post_share'),
    path(route='<int:post_id>/comment/', view=views.post_comment, name='post_comment'),
    path(route='tag/<slug:tag_slug>/', view=views.post_list, name='post_list_by_tag'),
    path(route='feed/', view=feeds.LatestPostsFeed(), name='post_feed')
]



