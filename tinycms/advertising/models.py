from django.db import models
from django.utils.translation import ugettext_lazy as _

class Advertising(models.Model):
    title       = models.CharField(_('title'), max_length=100)
    adv_title   = models.CharField(_('advertising title'), max_length=100)
    identifier  = models.CharField(_('identifier'), max_length=100, unique=True, help_text=_('Allow only letters and numbers.'))
    image       = models.ImageField(_('image'), upload_to = 'images/ad/%Y/%m', blank=True)
    link        = models.URLField(_('link'), max_length=255, blank=True)
    code        = models.TextField(_('code'), blank=True)
    description = models.TextField(_('description'), max_length=1500, blank=True)
    create_date = models.DateTimeField(_('create date'), auto_now_add=True, editable=False)
    start_date  = models.DateTimeField(_('start date'), null=True, blank=True)
    end_date    = models.DateTimeField(_('end date'), null=True, blank=True)
    active      = models.BooleanField(_('active'), default=True)

    def __unicode__(self):
        return "%s" % self.title

    class Meta:
        verbose_name = _('Advertising')
        verbose_name_plural = _('Advertisings')

_('Advertising')

class Media(models.Model):
    title   = models.CharField(_('title'), max_length=100)
    image   = models.ImageField(_('image'), upload_to = 'images/ad/%Y/%m', blank=True)
    ad      = models.ForeignKey(Advertising, verbose_name=_('advertising'), related_name="ad_medias")

_('Media')
