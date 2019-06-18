import random
import string
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import redirect, render, reverse, get_object_or_404
from django.views import generic

from helpers import AuthorRequiredMixin, get_page_list
from youtube.settings import ALLOWED_HOSTS, EMAIL_HOST_USER
from .forms import ProfileForm, SignUpForm, UserLoginForm, ChangePwdForm, ResetPwdForm

User = get_user_model()


def login(request):
    if 'POST' == request.method:
        next_url = request.POST.get('next', '/')
        form = UserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                # return redirect('home')
                return redirect(next_url)
        else:
            print(form.errors)
    else:
        next_url = request.GET.get('next', '/')
        form = UserLoginForm()
    print(next_url)
    return render(request, 'users/login.html', {'form': form, 'next': next_url})


def signup(request):
    if 'POST' == request.method:
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password1 = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password1)
            auth_login(request, user)
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect('home')


def change_password(request):
    if 'POST' == request.method:
        form = ChangePwdForm(request.user, request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if not user.is_staff and not user.is_superuser:
                user.save()
                update_session_auth_hash(request, user)  # 更新session 非常重要！
                messages.success(request, '修改成功')
                return redirect('users:change_password')
            else:
                messages.warning(request, '无权修改管理员密码')
                return redirect('users:change_password')
        else:
            print(form.errors)
    else:
        form = ChangePwdForm(request.user)
    return render(request, 'users/change_password.html', {'form': form})


class ProfileView(LoginRequiredMixin, AuthorRequiredMixin, generic.UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'users/profile.html'

    def get_success_url(self):
        messages.success(self.request, '保存成功')
        return reverse('users:profile', kwargs={'pk': self.request.user.pk})


class LikeListView(generic.ListView):
    model = User
    template_name = 'users/like_videos.html'
    context_object_name = 'video_list'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LikeListView, self).get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        page_list = get_page_list(paginator, page)
        context['page_list'] = page_list
        return context

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        videos = user.liked_videos.all().order_by('pk')
        return videos


def reset_password(request):
    if 'POST' == request.method:
        form = ResetPwdForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            try:
                user = User.objects.get(username=username, email=email)
                if user is not None:
                    token = str(hash(datetime.now()))
                    user.first_name = token[:10]
                    user.last_name = token[10:]
                    user.save()
                    send_email(token, email)
                    return render(request, 'users/reset_password_email.html')
            except User.DoesNotExist:
                messages.error(request, '用户名和邮箱地址不匹配')
        else:
            print(form.errors)
    else:
        form = ResetPwdForm()
    return render(request, 'users/reset_password.html', {'form': form})


def reset_password_done(request):
    token = request.GET.get('token', None)
    if token is None or len(token) < 10:
        messages.error(request, '无效的请求')
        return render(request, 'users/reset_error.html')
    try:
        user = User.objects.get(first_name=token[:10], last_name=token[10:])
        if user is not None:
            random_password = random_string()
            user.set_password(random_password)
            user.save()
            messages.info(request, '新密码：{}'.format(random_password))
            return render(request, 'users/reset_password_done.html')
    except User.DoesNotExist:
        messages.error(request, '无效的请求')
        return render(request, 'users/reset_error.html')


def random_string():
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(8))


def send_email(token, email):
    host = '127.0.0.1:8000'
    if len(ALLOWED_HOSTS) > 0:
        host = ALLOWED_HOSTS[0]
    html_link = 'http://{0}/users/reset_password_done/?token={1}'.format(host, token)
    subject = 'PassLineMovie用户密码重设'
    message = '如果这不是您本人的操作，请忽略此邮件'
    html_message = '<p><a href="{}">点我</a>进行密码重设。为了您的账户安全，请勿向把链接发给他人！</p>'.format(html_link)
    send_mail(subject, message, EMAIL_HOST_USER, [email], html_message=html_message)
