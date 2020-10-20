from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm
)
from django.contrib.auth import get_user_model
from django.db import transaction
from .models import User, Student

from django.forms import ModelForm

#User = get_user_model()

User = User
Student = Student


class LoginForm(AuthenticationForm):
    """ログインフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label  # placeholderにフィールドのラベルを入れる


class UserCreateForm(UserCreationForm):
    """ユーザー登録用フォーム"""

    class Meta:
        model = User
        fields = ( 'school_name', 'email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        return email

#追加----------------------------------------------------------------------
    @transaction.atomic
    def save(self,commit=True):
        user = super().save(commit=False)
        user.is_society = True
        user.save()
        return user
#-------------------------------------------------------------------------


class StudentCreateForm(UserCreationForm):
#class StudentCreateForm(ModelForm):

    class Meta: #(UserCreationForm.Meta):
        # Userでokそう
        model = User
        #model = Student
        fields = ('email', )

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        return email
    

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        #student.interests.add(*self.cleaned_data.get('interests'))
        return user
    
