from django.db import models
from django.contrib.comments.models import Comment
from django.utils.translation import ugettext_lazy as _

class CommentMod(Comment):
    title = models.CharField(_('title'), max_length=300)
    phone = models.CharField(_('phone'), max_length=64, blank=True)

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')

_('CommentMod')
