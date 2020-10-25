from django.urls import path
from . import views
from .views import (
    selectfunc, loginfunc, student_home, society_home, company_home, SignUpView, detailfunc, goodfunc,
    StudentProfileDetailView, view_societies
)

app_name = 'app'

urlpatterns = [
    path('',selectfunc,name='select'),
    path('login/', loginfunc, name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),

    path('signup/', SignUpView.as_view(), name='signup'),
    path('user_create/', views.UserCreate.as_view(), name='user_create'),
    path('student_create/', views.StudentCreate.as_view(), name='student_create'),
    path('company_create/', views.CompanyCreate.as_view(), name='company_create'),
    path('user_create/done', views.UserCreateDone.as_view(), name='user_create_done'),
    path('user_create/complete/<token>/', views.UserCreateComplete.as_view(), name='user_create_complete'),
    
    path('student_home/',student_home,name='student_home'),
    path('society_home',society_home,name='society_home'),
    path('company_home',company_home,name='company_home'),

    path('student_home/view_societies/',view_societies,name='view_societies'),

    path('detail/<int:pk>', detailfunc, name='detail'),
    path('good/<int:pk>', goodfunc, name='good'),

    path('<str:username>', views.StudentProfileDetailView.as_view(), name='profile'),
    #path('<slug:username>/edit', views.StudentProfileUpdateView.as_view(), name='edit'),

    path('<slug:username>/follow', views.follow_view, name='follow'),
    path('<slug:username>/unfollow', views.unfollow_view, name='unfollow'),


    # 不要
    #path('login/', views.Login.as_view(), name='login'),
    #path('user_create/', create_user, name='user_create'),
    #path('signup2/', create_user , name='signup2'),
    #path('list/', listfunc, name='list'),
]