from django.shortcuts import render, redirect, get_object_or_404 #追加
from .forms import SignUpForm
from django.contrib.auth import authenticate, login
from blog_app .models import Post
from django.contrib.auth.models import User

def detail(request, user_id):
   user = get_object_or_404(User, id=user_id)
   posts = user.post_set.all().order_by('-created_at') # PostモデルとUserモデルを紐づける事で、直感的にユーザーの記事を取得。
   return render(request, 'user_app/detail.html', {'user': user, 'posts': posts})

def edit(request, user_id):
   user = get_object_or_404(User, id=user_id)
   if request.method == "POST":
       form = SignUpForm(request.POST, instance=request.user)
       if form.is_valid():
           form.save()
           return redirect('user_app:detail', user_id=user.id)
   else:
       form = SignUpForm(instance=user)
   return render(request, 'user_app/edit.html', {'form': form, 'user':user })

# Create your views here.
def signup(request):
  signup_form = SignUpForm(request.POST or None) # 新規登録ページに遷移したのか、POSTメソッドでフォームの内容が送信されたのか判別。その結果をsignup_form変数に代入。
  if request.method == "POST" and signup_form.is_valid(): # メソッドがPOSTで尚且つ送信されたデータの内容にエラーがないか確認。
      user = signup_form.save() # 保存後、user変数に代入
      input_username = signup_form.cleaned_data['username']
      input_email = signup_form.cleaned_data['email']
      input_password = signup_form.cleaned_data['password1']
      user = authenticate(username=input_username, email=input_email, password=input_password) # input_...変数を認証。
      login(request, user) # 新規登録完了かつログイン状態
      return redirect('blog_app:index')
  context = {
      "signup_form": signup_form,
  }
  return render(request, 'user_app/signup.html', context)

def delete(request, user_id):
   user = get_object_or_404(User, id=user_id)
   user.delete()
   return redirect('blog_app:index')
# 削除用のテンプレートは用意しないので、ユーザーの編集ページ内(user_app/edit.html)に退会ボタンを設置。