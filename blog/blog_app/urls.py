from django.urls import path
from . import views # '.'同じ階層(フォルダ)内のviews.pyを呼び出す

app_name = 'blog_app'
urlpatterns = [
    path('', views.index, name='index'), # path('http://127.0.0.1:8000/',viewsファイル,index関数,name='index')name='index'はサイト内にリンクを設置するときに使用
    path('detail/<int:post_id>/', views.detail, name='detail'),
    # detail/<int:post_id>/の部分は、記事の詳細をpostのid番号で把握するため<int:post_id>を使用。ex)http://127.0.0.1:8000/detail/1/
    path('add/', views.add, name='add'),
    path('edit/<int:post_id>/', views.edit, name='edit'),
    path('delete/<int:post_id>/', views.delete, name='delete'),
]