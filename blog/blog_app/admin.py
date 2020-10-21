# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Post, Tag
# Register your models here.

admin.site.register(Post) # 管理者画面(admin)にPostモデルを登録(register)
admin.site.register(Tag) # Post同様