from django import forms
from django.contrib.comments.forms import CommentForm
from tinycms.commentmod.models import CommentMod
from django.utils.translation import ugettext_lazy as _

from django.conf import settings

COMMENT_MAX_LENGTH  = getattr(settings, 'COMMENT_MAX_LENGTH', 3000)
REQUIRE_EMAIL       = getattr(settings, 'REQUIRE_EMAIL', True)
REQUIRE_NAME        = getattr(settings, 'REQUIRE_NAME', True)

class CommentFormMod(CommentForm):
    title       = forms.CharField(label=_('title'), max_length=300)
    phone       = forms.CharField(label=_('phone'), max_length=64, required=False)

    if REQUIRE_NAME:
        name    = forms.CharField(label=_('callName'), max_length=50)
    else:
        name    = forms.CharField(label=_('callName'), max_length=50, required=False)

    if REQUIRE_EMAIL:
        email   = forms.EmailField(label=_("Email address"))
    else:
        email   = forms.EmailField(label=_("Email address"), required=False)

    def __init__(self, *args, **kwargs):
        super(CommentFormMod, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['title', 'comment', 'name', 'phone', 'email', 'content_type', 'object_pk', 'timestamp', 'security_hash', 'url', 'honeypot']

    def get_comment_model(self):
        # Use our custom comment model instead of the built-in one.
        return CommentMod

    def get_comment_create_data(self):
        # Use the data of the superclass, and add in the title field
        data = super(CommentFormMod, self).get_comment_create_data()
        data['title'] = self.cleaned_data['title']
        data['phone'] = self.cleaned_data['phone']
        return data
