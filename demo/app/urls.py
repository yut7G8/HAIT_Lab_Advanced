from django.urls import path
from . import views
from .views import selectfunc, listfunc, selectlogin

app_name = 'app'

urlpatterns = [
    path('',selectfunc,name='select'),
    #path('login/', loginfunc, name='login'),
    path('select_login', selectlogin, name='select_login'),
    path('user_login/', views.StudentLogin.as_view(), name='user_login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('user_create/', views.StudentCreate.as_view(), name='user_create'),
    path('user_create/done', views.StudentCreateDone.as_view(), name='user_create_done'),
    path('user_create/complete/<token>/', views.StudentCreateComplete.as_view(), name='user_create_complete'),
    path('list/',listfunc,name='list'),

    path('society_login/', views.SocietyLogin.as_view(), name='society_login'),
    path('society_create/', views.SocietyCreate.as_view(), name='society_create'),
    path('society_create/done', views.SocietyCreateDone.as_view(), name='society_create_done'),
    path('society_create/complete/<token>/', views.SocietyCreateComplete.as_view(), name='society_create_complete'),
]