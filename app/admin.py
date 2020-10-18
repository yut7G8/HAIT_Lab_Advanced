from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _
from .models import User, Student, Society


class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)


class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        #(_('Personal info'), {'fields': ('first_name', 'last_name','grade','school_name')}),
        (_('Personal info'), {'fields': ('school_name', )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    #list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_display = ('email', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    #search_fields = ('email', 'first_name', 'last_name')
    search_fields = ('email',)
    ordering = ('email',)



class MyStudentChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


class MyStudentCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)


class MyStudentAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name','grade','school_name')}),
        #(_('Personal info'), {'fields': ('school_name', )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    #list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_display = ('email', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    #search_fields = ('email', 'first_name', 'last_name')
    search_fields = ('email',)
    ordering = ('email',)


class MySocietyChangeForm(UserChangeForm):
    class Meta:
        model = Society
        fields = '__all__'


class MySocietyCreationForm(UserCreationForm):
    class Meta:
        model = Society
        fields = ('email',)


class MySocietyAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('society_name','school_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    form = MySocietyChangeForm
    add_form = MySocietyCreationForm
    list_display = ('email', 'society_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'society_name')
    ordering = ('email',)


admin.site.register(User, MyUserAdmin)
admin.site.register(Student, MyStudentAdmin)
admin.site.register(Society, MySocietyAdmin)