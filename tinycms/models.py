import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField

from conf import settings as tinycms_settings

class Category(MPTTModel):
    parent          = TreeForeignKey('self', null=True, blank=True, related_name="children", verbose_name='Parent')
    name            = models.CharField(_("name"), max_length=100)
    slug            = models.SlugField(_("slug"))
    url             = models.CharField(_("url"), blank=True, max_length=255, help_text=_("An URL to use instead of the one derived from the category hierarchy."))
    active          = models.BooleanField(_("active"), default=True)
    order           = models.IntegerField(_("order"), default=50)
    description     = models.TextField(_("description"), blank=True, null=True)
    marker          = models.CharField(_("marker"), max_length=100, blank=True)
    template        = models.CharField(_('category template'), max_length=255, blank=True, default="")
    meta_keywords   = models.CharField(_("keywords"), blank=True, default="", max_length=255, help_text=_("Comma-separated keywords for search engines."))
    meta_extra      = models.TextField(_("extra"), blank=True, default="", help_text=_("(Advanced) Any additional HTML to be placed verbatim in the &lt;head&gt;"))
    create_date     = models.DateTimeField(_('create date'), auto_now_add=True, editable=False)

    def __unicode__(self):
        return "%s" % self.name

    def get_absolute_url(self):
        if self.active:
            if self.url:
                return self.url
            else:
                p = self
                u = ''
                for i in range(self.level, 0, -1):
                    u = "%s/%s" % (p.slug, u)
                    p = p.parent
                return "/%s" % u

    def clean(self):
        if self.get_siblings(include_self=False).filter(slug__exact=self.slug):
            raise ValidationError(_('This slug already exist in this level.'))

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

_("Categories")

class Symbol(models.Model):
    name        = models.CharField(_("name"), max_length=100)
    symbol      = models.CharField(_("symbol"), max_length=20)
    description = models.TextField(_("description"), blank=True, null=True)
    is_default  = models.BooleanField(_('is default'), default=False)

    def __unicode__(self):
        return "%s[%s]" % (self.name, self.symbol)

    class Meta:
        verbose_name = _('symbol')
        verbose_name_plural = _('symbols')

def get_default_symbol():
    return Symbol.objects.filter(is_default=True)

class TitleClass(models.Model):
    name        = models.CharField(_("name"), max_length=100)
    title_class = models.CharField(_("title class"), max_length=20)
    description = models.TextField(_("description"), blank=True, null=True)

    def __unicode__(self):
        return "%s[%s]" % (self.name, self.title_class)

    class Meta:
        verbose_name = _('title class')
        verbose_name_plural = _('title classes')

class EntryBase(models.Model):
    author              = models.ForeignKey(User, verbose_name=_('author'), related_name="entry_author")
    modified_by         = models.ForeignKey(User, verbose_name=_('modified by'), related_name="modified_by", blank=True, null=True)
    title               = models.CharField(_('title'), max_length=255)
    titleclass          = models.ManyToManyField(TitleClass, verbose_name=_('title class'), blank=True, null=True)
    alternate_title     = models.CharField(_('alternate title'), max_length=255, blank=True, default="")
    jump                = models.BooleanField(_('jump'), default=False)
    jump_to_url         = models.CharField(_('jump to url'), blank=True, default="", max_length=255)
    slug                = models.SlugField(_('slug'), blank=True, default="", help_text=_('default is the id of entry.'))
    category            = TreeForeignKey(Category, verbose_name=_('category'), related_name="entry_category")
    sub_category        = TreeManyToManyField(Category, verbose_name=_('sub_category'), related_name="sub_category", blank=True, null=True)
    source              = models.CharField(_('source'), max_length=100, blank=True, default="")
    thumbnail           = models.ImageField(_('thumbnail'), upload_to = 'images/thumbs/%Y/%m/%d', blank=True)
    alternate_thumbnail = models.ImageField(_('alternate_thumbnail'), upload_to = 'images/thumbs/%Y/%m/%d', blank=True)
    description         = models.TextField(_("description"), max_length=1500, blank=True)
    symbol              = models.ManyToManyField(Symbol, verbose_name=_('symbol'), default=get_default_symbol, blank=True, null=True)
    publish             = models.BooleanField(_('publish'), default=tinycms_settings.PUBLISH_DEFAULT)
    publisher           = models.ForeignKey(User, verbose_name=_('publisher'), related_name="entry_publisher", blank=True, null=True)
    create_date         = models.DateTimeField(_('create date'), auto_now_add=True, editable=False)
    pub_date            = models.DateTimeField(_('publish date'), default=datetime.datetime.now)
    mod_time            = models.DateTimeField(_('modification time'), auto_now=True)
    allow_comment       = models.BooleanField(_('allow comment'), default=True)
    is_draft            = models.BooleanField(_('is draft'), default=tinycms_settings.DRAFT_DEFAULT)
    meta_keywords       = models.CharField(_("keywords"), blank=True, default="", max_length=255, help_text=_("Comma-separated keywords for search engines."))
    meta_extra          = meta_extra = models.TextField(_("extra"), blank=True, default="", help_text=_("(Advanced) Any additional HTML to be placed verbatim in the &lt;head&gt;"))
    template            = models.CharField(_('entry template'), max_length=255, blank=True, default="")

    classname           = models.CharField(max_length=32, editable=False, null=True)

    def __unicode__(self):
        return "%s" % self.title

    def save(self, *args, **kwargs):
        self.classname = self.__class__.__name__
        self.save_base()

        try:
            hit = Hit.objects.get(entry=self)
        except Hit.DoesNotExist:
            Hit.objects.create(entry=self, hit=0)

    def get_concrete(self):
        return self.__getattribute__(self.classname.lower())

    def get_absolute_url(self):
        return "/%s/%s/" % (self.pub_date.strftime("%Y/%m/%d/%H"), self.pk)

    def get_preview_url(self):
        return "/preview/%s/" % self.pk

    def get_titleclass(self):
        titleclass = ""
        for tc in self.titleclass.all():
            titleclass = titleclass + tc.title_class + " "
        return titleclass.strip()

    class Meta:
        ordering = ['-pub_date', '-id']
        permissions = (
            ('publish_entry', _('Can publish entry')),
            ('view_all_entries', _('Can view all entries')),
        )

    class MPTTMeta:
        parent_attr = 'category'

class Article(EntryBase):
    content     = models.TextField(_("content"), blank=True)

    class Meta:
        verbose_name = _('article')
        verbose_name_plural = _('articles')

class Video(EntryBase):
    video_url = models.CharField(_('video url'), max_length=255)

    class Meta:
        verbose_name = _('video')
        verbose_name_plural = _('videos')

class Hit(models.Model):
    entry       = models.OneToOneField(EntryBase, verbose_name = _('entry'), editable=False)
    hit         = models.IntegerField(_('entry hit times'), default=0)
    last_time   = models.DateTimeField(_('last hit time'), auto_now=True)

    def __unicode__(self):
        return _("%s times") % (self.hit)

    class Meta:
        verbose_name = _('hit times')
        verbose_name_plural = verbose_name

class Media(models.Model):
    title           = models.CharField(_('title'), max_length=255)
    uploader        = models.ForeignKey(User, verbose_name=_('uploader'))
    image           = models.ImageField(_('image'), upload_to = 'images/%Y/%m/%d')
    upload_datetime = models.DateTimeField(_('upload date'), auto_now_add=True, editable=False)

    def __unicode__(self):
        return "%s" % self.title

