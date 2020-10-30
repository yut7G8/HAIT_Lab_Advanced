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
    LoginForm, UserCreateForm, StudentCreateForm, CompanyCreateForm
)
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from .models import User, Student, Company, BoardModel
from .decorators import student_required, society_required, company_required

from django.contrib.auth.forms import UserCreationForm


# ログイン前のページ表示
def selectfunc(request):
    return render(request,'select.html')


# signup時、studentかsocietyか選択
class SignUpView(TemplateView):
    template_name = 'signup.html'


# login
def loginfunc(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_login = User.objects.get(email=username)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user_login)
            if user_login.is_student:
                #return render(request, 'list.html')
                #return redirect('app:list')
                return redirect('app:student_home')
            if user_login.is_society:
                #return render(request, 'society_home.html')
                return redirect('app:society_home')
            if user_login.is_company:
                #return render(request, 'company_home.html')
                return redirect('app:company_home')
        else:
            return render(request, 'login.html', {'error':'メールアドレスかパスワードが間違っています'})
    else:
        return render(request, 'login.html')


# StudentUserのhome画面
@login_required
@student_required
def student_home(request):
    object_list = BoardModel.objects.all()
    return render(request, 'student_home.html', {'object_list':object_list})
    #return render(request,'student_home.html')


# SocietyUserのhome画面
@login_required
@society_required
def society_home(request):
    return render(request,'society_home.html')


# CompanyUserのhome画面
@login_required
@company_required
def company_home(request):
    return render(request,'company_home.html')


class Logout(LogoutView):
    """ログアウトページ"""
    template_name = 'select.html'


# SocietyUserのsignup
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


#StudentUserのsignup
class StudentCreate(generic.CreateView):
    model = User
    form_class = StudentCreateForm
    template_name = 'user_create.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        #login(self.request, user)
        #return redirect('app:list')。
    
        #user = form.save(commit=False)
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


#companyUserのsignup
class CompanyCreate(generic.CreateView):
    model = User
    form_class = CompanyCreateForm
    template_name = 'user_create.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'company'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        #login(self.request, user)
        #return redirect('app:list')。
    
        #user = form.save(commit=False)
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



# User(Society/Student)の仮登録
class UserCreateDone(generic.TemplateView):
    template_name = 'user_create_done.html'


# User(Society/Student)の本登録処理
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


# 各投稿の詳細ページに飛ぶ
def detailfunc(request):
    object = BoardModel.objects.all().order_by('-readtext') # BordModelモデルの記事（objects）を全て(all())作成された順番（order_by('-readtext')）に取得してobject変数に代入
    return render(request, 'detail.html', {'object':object})


# いいね機能の実装
def goodfunc(request, pk):
    post = BoardModel.objects.get(pk=pk)
    post.good = post.good + 1
    post.save()
    return redirect('app:student_home')