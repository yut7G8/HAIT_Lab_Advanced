from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

#from classroom.views import students, teachers

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),

    #path('accounts/', include('django.contrib.auth.urls')),
    #path('accounts/signup/', classroom.SignUpView.as_view(), name='signup'),
    #path('accounts/signup/student/', students.StudentSignUpView.as_view(), name='student_signup'),
    #path('accounts/signup/teacher/', teachers.TeacherSignUpView.as_view(), name='teacher_signup'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)