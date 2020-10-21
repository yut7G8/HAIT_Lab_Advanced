from django.urls import path
from . import views
from django.contrib.auth import views as auth_views # ログイン、ログアウト機能を簡単に実現

app_name = 'user_app'
urlpatterns = [
  path('login/', auth_views.LoginView.as_view(template_name='user_app/login.html'), name='login'), # urlがloginの場合にDjangoが用意するauth_views.LoginView.as_viewを使って専用のページを返す。
  path('logout/', auth_views.LogoutView.as_view(), name='logout'),
  path('signup/', views.signup, name='signup'),
  path('user/<int:user_id>/', views.detail, name='detail'),
  path('user/edit/<int:user_id>/', views.edit, name='edit'),
  path('user/delete/<int:user_id>/', views.delete, name='delete'),
]