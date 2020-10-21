# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404, redirect
# get_object_or_404関数のインポート
# 取得したidが存在しなかった場合、よく見かける「404 not found」をブラウザに返す。
from .forms import PostAddForm # PostAddFormクラスをインポート


from django.shortcuts import render
from .models import Post, Tag # Post,Tagモデルをviews.py内で使用するためにインポート。
# 同ディレクトリ内のmodels.pyのPost, Tag
# Create your views here.
def index(request):
    posts = Post.objects.all().order_by('-created_at')
    # Postモデルの記事(objects)を全て(all())作成された順番(order_by('-created_at'))に取得してposts変数に代入。
    return render(request, 'blog_app/index.html', {'posts': posts}) 
    # renderとは描画するという意味
    # データが代入されたpostsをrender関数に渡す。
    # post変数をテンプレート内で表示させるには、index.htmlに{{posts}}("{{変数名}}")とする。
# http://127.0.0.1:8000/ が呼び出され、blog_appのurls.pyに行き、このindex関数が呼び出され、blog_app内のindex.htmlを返す

def detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'blog_app/detail.html', {'post': post})
# detailの引数はurls.pyから送られてきたrequestとpost_idを取得
# 特定の記事を取得出来たら、post変数に代入にてreturnで返す

def add(request):
   if request.method == "POST": # リクエストがPOST(フォームのデータが正しく送られてきたとき)と等しい場合は結果が真 
       form = PostAddForm(request.POST, request.FILES) # 送られてきたデータをPostAddFormの引数で受け取り、form変数に代入する。画像などのファイルデータはrequest.FILESが必要。
       if form.is_valid(): # form変数内のデータに問題がないか検証。
           post = form.save(commit=False) # 検証後、save()関数で保存したい処だが、下のコードで、そのユーザーの投稿かを判断したい為、commit=Falseで仮登録にする。それをpost変数に代入。
           post.user = request.user # どのユーザーにrequestされたのかを判断して保存。
           post.save() # 記事の内容とユーザーの判別に成功したら、実際に保存。
           return redirect('blog_app:index') # redirect関数を使い、index.htmlに返す。
   else: # リクエストがPOSTではなかった場合
       form = PostAddForm()
   return render(request, 'blog_app/add.html', {'form': form})

def edit(request, post_id):
   post = get_object_or_404(Post, id=post_id)
   if request.method == "POST":
       form = PostAddForm(request.POST, request.FILES, instance=post)
       if form.is_valid():
           form.save()
           return redirect('blog_app:detail', post_id=post.id)
   else:
       form = PostAddForm(instance=post)
   return render(request, 'blog_app/edit.html', {'form': form, 'post':post })

def delete(request, post_id): # 削除機能はHTMLを作る必要はない。削除ボタンを詳細ページ(detail.html)に作成し、ボタンクリックで削除出来るようにする。
   post = get_object_or_404(Post, id=post_id)
   post.delete()
   return redirect('blog_app:index')