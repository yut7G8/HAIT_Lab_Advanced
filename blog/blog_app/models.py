# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models # 簡単にモデルの作成するためにインポート
from django.utils import timezone #追加
from django.contrib.auth.models import User # Userモデルのインポート

# Create your models here.
class Tag(models.Model):
 tag = models.CharField('タグ名', max_length=50)
 def __str__(self):
   return self.tag

class Post(models.Model): # クラスは大文字スタート
   title = models.CharField('タイトル', max_length=35) # フォームなどで使用されるlabelタグの設定を'タイトル'に
   text = models.TextField('本文')
   image = models.ImageField('画像', upload_to = 'images', blank=True) # upload_to = 'images'で画像登校時にimagesディレクトリが作成され、その中に画像が保存される。blank=Tureで画像がない投稿も可能に。
   created_at = models.DateTimeField('投稿日', default=timezone.now)
   tag = models.ForeignKey(Tag, verbose_name = 'タグ', on_delete=models.PROTECT)
# ForeignKey(外部キー)は他のモデルと紐づけるときに使用する。(紐付け方法は複数あり)
# Foreignkeyの第1引数は紐づけたいモデル名(ここではTag)
# 第2引数に管理者画面で表示させたい名前('タグ')
# 第3引数の設定、(on_delete=models.PROTECT)は記事を削除した際に紐づいているタグも一緒に削除するかどうかの設定。PROTECTなので、タグは一緒に削除されない。
   user = models.ForeignKey(User, on_delete=models.CASCADE) # Userモデルの紐づけ
   # on_delete=model.CASCADEは、もしユーザーが削除された場合、そのユーザーの記事も一緒に削除する設定
   def __str__(self):
       return self.title

# python manage.py makemigrations(マイグレーション)とは,models.pyに書いたクラスの内容を仮でDjangoにしらせること。
# ex) 出力結果
# Migrations for 'blog_app':
#  blog_app\migrations\0001_initial.py
#    - Create model Tag
#    - Create model Post

# 0001_initial.pyファイルをもとにテーブルを作成。間違いないか確認後、マイグレート。
# マイグレートとは？
# マイグレーションの段階で作成された0001_initial.pyファイルをDjangoに仮ではなく実際に適用

