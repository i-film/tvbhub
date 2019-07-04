from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm
from django.core.exceptions import ValidationError

from .models import User


def avatar_file_size(value):
    limit = 2 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('头像文件太大了，请限制在2M之内')


class SignUpForm(UserCreationForm):
    username = forms.CharField(min_length=2, max_length=30,
                               error_messages={'min_length': '用户名至少2个字', 'max_length': '用户名不能多于30个字',
                                               'required': '用户名不能为空', },
                               widget=forms.TextInput(attrs={'placeholder': '请输入用户名（2～30个字）'}))
    password1 = forms.CharField(min_length=8, max_length=16,
                                error_messages={'min_length': '密码至少8位', 'max_length': '密码不能多于16位',
                                                'required': '密码不能为空', },
                                widget=forms.PasswordInput(attrs={'placeholder': '请输入密码（8～16位）'}))
    password2 = forms.CharField(min_length=8, max_length=16,
                                error_messages={'min_length': '密码至少8位', 'max_length': '密码不能多于16位',
                                                'required': '密码不能为空（8～16位）', },
                                widget=forms.PasswordInput(attrs={'placeholder': '请确认密码（8～16位）'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2',)

    error_messages = {'password_mismatch': '两次密码不一致', }


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(min_length=2, max_length=30,
                               error_messages={'min_length': '用户名至少2个字', 'max_length': '用户名不能多于30个字',
                                               'required': '用户名不能为空', },
                               widget=forms.TextInput(attrs={'placeholder': '请输入用户名（2～30个字）'}))
    password = forms.CharField(min_length=8, max_length=16,
                               error_messages={'min_length': '密码至少8位', 'max_length': '密码不能多于16个字符',
                                               'required': '密码不能为空', },
                               widget=forms.PasswordInput(attrs={'placeholder': '请输入密码（8～16位）'}))

    class Meta:
        model = User
        fields = ['username', 'password']

    error_messages = {'invalid_login': '用户名或密码错误', }


class ChangePwdForm(PasswordChangeForm):
    old_password = forms.CharField(error_messages={'required': '现在的密码不能为空', },
                                   widget=forms.PasswordInput(attrs={'placeholder': '请输入现在的密码（8～16位）'}))
    new_password1 = forms.CharField(error_messages={'required': '请输入新密码', },
                                    widget=forms.PasswordInput(attrs={'placeholder': '请输入新密码（8～16位）'}))
    new_password2 = forms.CharField(error_messages={'required': '请确认新密码', },
                                    widget=forms.PasswordInput(attrs={'placeholder': '请输入确认密码（8～16位）'}))


class ResetPwdForm(PasswordResetForm):
    username = forms.CharField(min_length=2, max_length=30, required=False,
                               error_messages={'min_length': '用户名至少2个字', 'max_length': '用户名不能多于30个字', },
                               widget=forms.TextInput(attrs={'placeholder': '请输入用户名（2～30个字）'}))
    email = forms.EmailField(required=False, error_messages={'invalid': '请输入有效的邮箱地址', },
                             widget=forms.EmailInput(attrs={'placeholder': '请输入邮箱地址'}))


class ProfileForm(forms.ModelForm):
    username = forms.CharField(min_length=2, max_length=30, required=False,
                               error_messages={'min_length': '用户名至少2个字', 'max_length': '用户名不能多于30个字', },
                               widget=forms.TextInput(attrs={'placeholder': '请输入用户名（2～30个字）'}))
    avatar = forms.ImageField(required=False, validators=[avatar_file_size],
                              widget=forms.FileInput(attrs={'class': 'n'}))

    email = forms.EmailField(required=False, error_messages={'invalid': '请输入有效的邮箱地址', },
                             widget=forms.EmailInput(attrs={'placeholder': '请输入邮箱地址'}))

    class Meta:
        model = User
        fields = ['username', 'avatar', 'email']
