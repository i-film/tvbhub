from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from users.models import User
from videos.models import Video, Classification


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(min_length=2, max_length=15,
                               error_messages={'min_length': '用户名至少2个字', 'max_length': '用户名不能多于15个字',
                                               'required': '用户名不能为空', },
                               widget=forms.TextInput(attrs={'placeholder': '请输入用户名（2～15个字）'}))
    password = forms.CharField(min_length=8, max_length=16,
                               error_messages={'min_length': '密码不少于8位', 'max_length': '密码不能多于16位',
                                               'required': '密码不能为空', },
                               widget=forms.PasswordInput(attrs={'placeholder': '请输入密码（最少8位）'}))

    class Meta:
        model = User
        fields = ['username', 'password']

    error_messages = {'invalid_login': '用户名或密码错误', }


class VideoPublishForm(forms.ModelForm):
    title = forms.CharField(min_length=1, max_length=30, required=True,
                            error_messages={'min_length': '标题至少1个字', 'max_length': '标题不能多于30个字', 'required': '标题不能为空'},
                            widget=forms.TextInput(attrs={'placeholder': '请输入标题（1～30个字）'}))
    status = forms.CharField(min_length=1, max_length=1, required=False, widget=forms.HiddenInput(attrs={'value': '0'}))
    link = forms.CharField(max_length=100, required=True,
                           error_messages={'max_length': '外链接最多100个字符', 'required': '外链接不能为空'},
                           widget=forms.Textarea(attrs={'placeholder': '腾讯，优酷，爱奇艺等地址'}))

    class Meta:
        model = Video
        fields = ['title', 'status', 'classification', 'link', ]


class VideoEditForm(forms.ModelForm):
    title = forms.CharField(min_length=1, max_length=30, required=True,
                            error_messages={'min_length': '标题至少1个字', 'max_length': '标题不能多于30个字', 'required': '标题不能为空'},
                            widget=forms.TextInput(attrs={'placeholder': '请输入标题（1～30个字）'}))
    status = forms.CharField(min_length=1, max_length=1, required=False, widget=forms.HiddenInput())
    link = forms.CharField(max_length=100, required=True,
                           error_messages={'max_length': '外链接最多100个字符', 'required': '外链接不能为空'},
                           widget=forms.Textarea(attrs={'placeholder': '腾讯，优酷，爱奇艺等地址'}))

    class Meta:
        model = Video
        fields = ['title', 'status', 'classification', 'link', ]


class UserAddForm(forms.ModelForm):
    username = forms.CharField(min_length=2, max_length=30,
                               error_messages={'min_length': '用户名至少2个字', 'max_length': '用户名不能多于30个字',
                                               'required': '用户名不能为空', },
                               widget=forms.TextInput(attrs={'placeholder': '请输入用户名（2～30个字）'}))
    password = forms.CharField(min_length=8, max_length=16,
                               error_messages={'min_length': '密码至少8位', 'max_length': '密码不能多于16位',
                                               'required': '密码不能为空', },
                               widget=forms.PasswordInput(attrs={'placeholder': '请输入密码（8～16位）'}))

    class Meta:
        model = User
        fields = ['username', 'password', 'is_staff']


def username_validate(value):
    if value == "admin":
        raise ValidationError('不能编辑超级管理员')


class UserEditForm(forms.ModelForm):
    username = forms.CharField(min_length=2, max_length=30, required=True, validators=[username_validate],
                               error_messages={'min_length': '用户名至少2个字', 'max_length': '用户名不能多于30个字',
                                               'required': '用户名不能为空'},
                               widget=forms.TextInput(attrs={'placeholder': '请输入用户名（2～30个字）'}))

    class Meta:
        model = User
        fields = ['username', 'is_staff']


class ClassificationAddForm(forms.ModelForm):
    title = forms.CharField(min_length=2, max_length=6, required=True,
                            error_messages={'min_length': '至少2个字', 'max_length': '不能多于6个字', 'required': '不能为空'},
                            widget=forms.TextInput(attrs={'placeholder': '请输入分类名称（2～6）个字'}))

    class Meta:
        model = Classification
        fields = ['title', 'status']


class ClassificationEditForm(forms.ModelForm):
    title = forms.CharField(min_length=2, max_length=6, required=True,
                            error_messages={'min_length': '至少2个字', 'max_length': '不能多于6个字', 'required': '不能为空'},
                            widget=forms.TextInput(attrs={'placeholder': '请输入分类名称（2～6）个字'}))

    class Meta:
        model = Classification
        fields = ['title', 'status']
