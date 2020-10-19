from django.urls import path
from . import views
from .views import selectfunc,loginfunc,listfunc,SignUpView, create_user

app_name = 'app'

urlpatterns = [
    path('',selectfunc,name='select'),
    #path('login/', loginfunc, name='login'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('user_create/', views.UserCreate.as_view(), name='user_create'),
    path('user_create/done', views.UserCreateDone.as_view(), name='user_create_done'),
    path('user_create/complete/<token>/', views.UserCreateComplete.as_view(), name='user_create_complete'),
    path('list/',listfunc,name='list'),
    path('signup/', SignUpView.as_view(), name='signup'),

    path('student_create/', views.StudentCreate.as_view(), name='student_create'),
    #path('user_create/', create_user, name='user_create'),
]