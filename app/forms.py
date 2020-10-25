from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm
)
from django.contrib.auth import get_user_model
from django.db import transaction
from .models import User, Student, Company, BoardModel

from django.core.exceptions import ValidationError
from django.core.validators import validate_email

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


# SocietyUserのsignup
class UserCreateForm(UserCreationForm):
    """ユーザー登録用フォーム"""

    class Meta:
        model = User
        fields = ( 'school_name', 'society_name', 'email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        return email

    @transaction.atomic
    def save(self,commit=True):
        user = super().save(commit=False)
        user.is_society = True
        user.save()
        return user


# StudentUserのsignup
class StudentCreateForm(UserCreationForm):

    class Meta: #(UserCreationForm.Meta):
        # Userでokそう
        model = User
        #model = Student
        fields = ('first_name', 'last_name', 'email', )

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
        return user


# CompanyUserのsignup
class CompanyCreateForm(UserCreationForm):

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
        user.is_company = True
        user.save()
        company = Company.objects.create(user=user)
        return user
    

# Student用Profile編集
class StudentProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': "姓"}),)
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': "名"}),)
    school_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': "学校名"}),)
    grade = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': "学年"}),)
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': "メールアドレス"}),)
    #username = forms.CharField(max_length=50, widget=forms.TimeInput(attrs={'placeholder': "ユーザーID"}),)
    about_me = forms.CharField(widget=forms.Textarea(attrs={'size': 50}),)

    class Meta:
        model = User
        #fields = ('name', 'email', 'username', 'about_me',)
        fields = ('first_name', 'last_name', 'school_name', 'grade', 'email', 'about_me',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data["email"]

        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("正しいメールアドレスを指定してください")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        else:
            if self.user.email == email:
                return email

            raise ValidationError("このメールアドレスは既に使用されています")
