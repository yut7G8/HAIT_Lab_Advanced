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
    LoginForm, UserCreateForm, StudentCreateForm, SocietyCreateForm
)
from django.contrib.auth.decorators import login_required
from .models import User, Student, Society

#User = get_user_model()
User = User
Student = Student
Society = Society

def selectfunc(request):
    return render(request,'select.html')

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
            return redirect('user_login')

    return render(request, 'user_login.html')
'''

#@login_required
def listfunc(request):
    print('hello')
    print(type(request.user))
    return render(request,'list.html')

def selectlogin(request):
    return render(request, 'select_login.html')

class UserLogin(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'user_login.html'

class StudentLogin(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'user_login.html'

class SocietyLogin(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'society_login.html'


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
        message = render_to_string('app/mail_template/create/message_for_user.txt', context)

        user.email_user(subject, message)
        return redirect('app:user_create_done')

class StudentCreate(generic.CreateView):
    """ユーザー仮登録"""
    template_name = 'user_create.html'
    form_class = StudentCreateForm

    def form_valid(self, form):
        """仮登録と本登録用メールの発行."""
        # 仮登録と本登録の切り替えは、is_active属性を使うと簡単です。
        # 退会処理も、is_activeをFalseにするだけにしておくと捗ります。
        student = form.save(commit=False)
        student.is_active = False
        student.save()

        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(student.pk),
            'user': student,
        }

        subject = render_to_string('app/mail_template/create/subject.txt', context)
        message = render_to_string('app/mail_template/create/message_for_user.txt', context)

        student.email_user(subject, message)
        return redirect('app:user_create_done')


class SocietyCreate(generic.CreateView):
    """ユーザー仮登録"""
    template_name = 'user_create.html'
    form_class = SocietyCreateForm

    def form_valid(self, form):
        """仮登録と本登録用メールの発行."""
        # 仮登録と本登録の切り替えは、is_active属性を使うと簡単です。
        # 退会処理も、is_activeをFalseにするだけにしておくと捗ります。
        society = form.save(commit=False)
        society.is_active = False
        society.save()

        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(society.pk),
            'user': society,
        }

        subject = render_to_string('app/mail_template/create/subject.txt', context)
        message = render_to_string('app/mail_template/create/message_for_society.txt', context)

        society.email_user(subject, message)
        return redirect('app:user_create_done')


class UserCreateDone(generic.TemplateView):
    """ユーザー仮登録したよ"""
    template_name = 'user_create_done.html'

class StudentCreateDone(generic.TemplateView):
    """ユーザー仮登録したよ"""
    template_name = 'user_create_done.html'

class SocietyCreateDone(generic.TemplateView):
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


class StudentCreateComplete(generic.TemplateView):
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
                student = Student.objects.get(pk=user_pk)
            except Student.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not student.is_active:
                    # 問題なければ本登録とする
                    student.is_active = True
                    student.save()
                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()


class SocietyCreateComplete(generic.TemplateView):
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
                society = Society.objects.get(pk=user_pk)
            except Society.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not society.is_active:
                    # 問題なければ本登録とする
                    society.is_active = True
                    society.save()
                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()
