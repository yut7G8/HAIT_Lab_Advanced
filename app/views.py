from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView, LogoutView
)
from django.contrib.auth import authenticate, login,logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import redirect,render
from django.template.loader import render_to_string
from django.views import generic
from .forms import (
    LoginForm, UserCreateForm, StudentCreateForm
)
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from .models import User, Student
from .decorators import student_required, society_required

from django.contrib.auth.forms import UserCreationForm

#User = get_user_model()


def selectfunc(request):
    return render(request,'select.html')

#追加-----------------------------------------
class SignUpView(TemplateView):
    template_name = 'signup.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('app:list')
        else:
            return redirect('app:list')
    return render(request, 'select.html')
#-------------------------------------------------------

'''
def loginfunc(request):
    if request.method == 'POST':
        print(request.POST)
        username2 = request.POST['username']
        password2 = request.POST['password']
        user = authenticate(request, email=username2, password=password2)

        if user is not None:
            login(request, user)
            return render(request,'list.html')
        
        else:
            return redirect('login')

    return render(request, 'login.html')
'''

def loginfunc(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_login = User.objects.get(email=username)
        user = authenticate(username=username, password=password)
        #print(user_login.is_student)
        #print(user_login.is_society)
        if user is not None:
            login(request, user_login)
            if user_login.is_student:
            #if user_login.student.is_student:
                return render(request, 'list.html')
            if user_login.is_society:
                return render(request, 'list2.html')
        else:
            #return render(request, 'select.html')
            return render(request, 'login44.html', {'error':'メールアドレスかパスワードが間違っています'})
    else:
        return render(request, 'login44.html')


#@login_required
def listfunc(request):
    return render(request,'list.html')

class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'login.html'


class Logout(LogoutView):
    """ログアウトページ"""
    template_name = 'select.html'


class UserCreate(generic.CreateView):
    """ユーザー仮登録"""
    template_name = 'user_create.html'
    form_class = UserCreateForm

    def form_valid(self, form):
        """仮登録と本登録用メールの発行."""
        # 仮登録と本登録の切り替えは、is_active属性を使うと簡単です。
        # 退会処理も、is_activeをFalseにするだけにしておくと捗ります。
    
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }

        subject = render_to_string('app/mail_template/create/subject.txt', context)
        message = render_to_string('app/mail_template/create/message.txt', context)

        user.email_user(subject, message)
        return redirect('app:user_create_done')


class UserCreateDone(generic.TemplateView):
    """ユーザー仮登録したよ"""
    template_name = 'user_create_done.html'


class UserCreateComplete(generic.TemplateView):
    """メール内URLアクセス後のユーザー本登録"""
    template_name = 'user_create_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        """tokenが正しければ本登録."""
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 問題なければ本登録とする
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()



class StudentCreate(generic.CreateView):
    model = User
    form_class = StudentCreateForm
    template_name = 'user_create.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('students:quiz_list')



def create_user(request):
    if request.method == 'POST':
        user_form = UserCreateForm(request.POST)
        student_form = StudentCreateForm(request.POST)
        if  user_form.is_valid() and student_form.is_valid():
            user = user_form.save()
            student = student_form.save(commit=False)
            student.user = user
            student.save()
            return redirect('app:user_create_done')
    else:
        user_form = UserCreateForm()
        student_form = StudentCreateForm()
    return render(
        request,
        'user_create_done.html',
        {'user_create': user_form, 'student_create': student_form}
    )
