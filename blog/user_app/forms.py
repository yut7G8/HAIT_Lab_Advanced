from django import forms
from django.contrib.auth.forms import UserCreationForm # UserCreationFormをインポートすることで、Djangoがデフォルトで用意しているユーザー登録用のフォームが使用可能に。
from django.contrib.auth.models import User # Userモデルのインポート

class SignUpForm(UserCreationForm):
  class Meta:
      model = User
      fields = ('username', 'email', 'password1', 'password2')

# Djangoでは、認証機能は用意されているが、新規登録などは自身で作る必要がある。