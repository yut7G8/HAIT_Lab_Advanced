from django import forms
from .models import Post, Tag # Post, Tagモデルをインポート
from django.forms import ModelForm # モデルの参照。モデル内のtitle,text,imageなどのカラムを使用。

class PostAddForm(forms.ModelForm): # views.pyで実際にテンプレートにフォームを出力。    
   class Meta:
       model = Post # model変数にPostモデルを代入。
       fields = ['title', 'text', 'image', 'tag'] # fields変数にフォームで使うラベルを書く。

# モデルを元にフォームを作成