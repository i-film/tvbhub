from django import forms

from comments.models import Comment


class CommentForm(forms.ModelForm):
    content = forms.CharField(error_messages={'required': '评论不能为空', },
                              widget=forms.Textarea(attrs={'placeholder': '请输入评论内容（200个字以内）'}))

    class Meta:
        model = Comment
        fields = ['content']
