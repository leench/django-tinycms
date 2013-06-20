import datetime

try:
    import json
except ImportError:
    from django.utils import simplejson as json

from django.contrib import admin
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.widgets import AdminFileWidget
from django.contrib.admin import SimpleListFilter
from django.utils.encoding import force_unicode
from django.contrib.admin import helpers
from django.template.response import TemplateResponse

from mptt.admin import MPTTModelAdmin

from models import Category, EntryBase, Article, Video, Symbol, TitleClass, Hit, Media
from conf import settings as tinycms_settings

class CategoryAdmin(MPTTModelAdmin):
    list_display = ('pk', 'name', 'get_absolute_url_link', 'tree_id', 'lft', 'rght', 'level', 'parent', 'slug', 'active', 'create_date')
    list_display_links = ('name', )

    def get_absolute_url_link(self, obj):
        u = '<a href="../../r/%s/%s/" target="_blank">%s</a>' % (ContentType.objects.get(model="category").id, obj.id, obj.get_absolute_url())
        return mark_safe(u)
    get_absolute_url_link.short_description = _('absolute url')
    get_absolute_url_link.allow_tags = True

class AdminThumbWidget(AdminFileWidget):
    def __init__(self, attrs={}):
        super(AdminThumbWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        output = []
        if value and hasattr(value, "url"):
            output.append(('<a target="_blank" href="%s">'
                           '<img src="%s" style="height: 60px;" /></a> '
                           % (value.url, value.url)))
        output.append(super(AdminThumbWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))

class CategoryListFilter(SimpleListFilter):
    title = _('category(include children)')
    parameter_name = 'cic'

    def lookups(self, request, model_admin):
        categories = Category.objects.all()
        clist = []
        for c in categories:
            name = c.get_level()*'---'+c.name+'('+str(EntryBase.objects.filter(category__pk=c.pk).count())+')'
            clist.append((c.pk, name))
        return clist

    def queryset(self, request, queryset):
        if self.value():
            try:
                c = Category.objects.get(pk=self.value())
            except Category.DoesNotExist:
                return queryset
            return queryset.filter(category__lft__gte=c.lft, category__rght__lte=c.rght)
        else:
            return queryset

class EntryBaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'preview', 'true_url', 'category', 'thumb', 'get_symbols', 'publish', 'is_draft', 'pub_date', 'author', 'modified_by', 'publisher')
    list_display_links = ('title', )
    exclude = ('author', 'publisher', 'modified_by')
    actions = ['publish', 'unpublish', 'change_category', 'add_symbol', 'delete_symbol', ]
    search_fields = ['title', 'alternate_title', ]
    list_per_page = 40
    filter_horizontal = ('symbol', 'sub_category', )
    list_filter = ('author', 'publish', 'is_draft', CategoryListFilter, 'category', 'symbol')
    date_hierarchy = 'pub_date'
    formfield_overrides = {
        models.ImageField: {'widget': AdminThumbWidget},
    }

    def preview(self, obj):
        return _('<a href="%s" target="_blank">preview</a>') % obj.get_preview_url()
    preview.allow_tags = True
    preview.short_description = _('preview')

    def true_url(self, obj):
        if obj.publish:
            u = '<a href="../../r/%s/%s/" target="_blank">URL</a>' % (ContentType.objects.get(model="entrybase").id, obj.id)
            return mark_safe(u)
        return _('not published')
    true_url.allow_tags = True
    true_url.short_description = _('true url')

    def thumb(self, obj):
        if obj.thumbnail or obj.alternate_thumbnail:
            return _('True')
        else:
            return _('False')
    thumb.short_description = _('thumb')

    def get_symbols(self, obj):
        s = obj.symbol.all()
        return ', '.join(x.name for x in s)
    get_symbols.short_description = _('symbols')

    def queryset(self, request):
        qs = super(EntryBaseAdmin, self).queryset(request)
        if request.user.is_superuser or request.user.has_perm('entries.view_all_entries'):
            return qs
        return qs.filter(author=request.user)

    def save_model(self, request, obj, form, change):
        now = datetime.datetime.now()
        if obj.pub_date > now:
            obj.publish = False
        if change:
            obj.modified_by = request.user
        else:
            obj.author = request.user

        if obj.is_draft:
            obj.publish = False
            obj.publisher = None
        else:
            if not tinycms_settings.PUBLISH_DEFAULT:
                if not request.user.has_perm('entries.publish_entry'):
                    obj.publish = False
                elif obj.publish:
                    obj.publisher = request.user
            else:
                if obj.publish:
                    obj.publisher = request.user
        obj.save()

    def publish(modeladmin, request, queryset):
        if request.user.has_perm('entries.publish_entry'):
            queryset.filter(is_draft=False).update(publish=True, publisher=request.user)
    publish.short_description =_('publish')

    def unpublish(modeladmin, request, queryset):
        if request.user.has_perm('entries.publish_entry'):
            queryset.update(publish=False, publisher=None)
    unpublish.short_description =_('unpublish')

    def change_category(modeladmin, request, queryset):
        #from django.core import serializers
        #s = serializers.serialize("json", queryset, stream=response)

        opts = modeladmin.model._meta
        app_label = opts.app_label

        # Check that the user has delete permission for the actual model
        #...

        categories = Category.objects.all()
        clist = []
        for c in categories:
            name = c.get_level()*'---'+c.name
            clist.append({'pk': c.pk, 'name': name})

        if request.POST.get('post'):
            n = queryset.count()
            if n:
                t_category = request.POST.get('t_category')
                if t_category:
                    c = Category.objects.get(pk=t_category)
                    queryset.update(category=c)
                    for obj in queryset:
                        modeladmin.log_change(request, obj, 'Change category.')
            return None

        if len(queryset) == 1:
            objects_name = force_unicode(opts.verbose_name)
        else:
            objects_name = force_unicode(opts.verbose_name_plural)

        title = _("Select category that you want change.")

        context = {
            "title": title,
            "objects_name": objects_name,
            'clist': clist,
            'queryset': queryset,
            "opts": opts,
            "app_label": app_label,
            'categories': Category.objects.filter(active=True),
            'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
        }

        return TemplateResponse(request, [
            "admin/%s/%s/change_selected_category_confirmation.html" % (app_label, opts.object_name.lower()),
            "admin/%s/change_selected_category_confirmation.html" % app_label,
            "admin/change_selected_category_confirmation.html"
        ], context, current_app=modeladmin.admin_site.name)
    change_category.short_description =_('change category')

    def add_symbol(modeladmin, request, queryset):
        opts = modeladmin.model._meta
        app_label = opts.app_label

        symbols = Symbol.objects.all()

        if request.POST.get('post'):
            n = queryset.count()
            if n:
                t_symbol = request.POST.getlist('t_symbol')
                if t_symbol:
                    symbollist = []
                    for symbol_pk in t_symbol:
                        symbol = Symbol.objects.get(pk=symbol_pk)
                        symbollist.append(symbol)
                    for entry in queryset:
                        entry.symbol.add(*symbollist)
            return None

        if len(queryset) == 1:
            objects_name = force_unicode(opts.verbose_name)
        else:
            objects_name = force_unicode(opts.verbose_name_plural)

        title = _("Select symbol(s) that you want add.")
        context = {
            "title": title,
            "objects_name": objects_name,
            'symbols': symbols,
            'queryset': queryset,
            "opts": opts,
            "app_label": app_label,
            'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
        }
        return TemplateResponse(request, [
            "admin/add_symbol_confirmation.html"
        ], context, current_app=modeladmin.admin_site.name)
    add_symbol.short_description =_('add symbol')

    def delete_symbol(modeladmin, request, queryset):
        opts = modeladmin.model._meta
        app_label = opts.app_label

        symbols = Symbol.objects.all()

        if request.POST.get('post'):
            n = queryset.count()
            if n:
                t_symbol = request.POST.getlist('t_symbol')
                if t_symbol:
                    symbollist = []
                    for symbol_pk in t_symbol:
                        symbol = Symbol.objects.get(pk=symbol_pk)
                        symbollist.append(symbol)
                    for entry in queryset:
                        entry.symbol.remove(*symbollist)
                return None

        if len(queryset) == 1:
            objects_name = force_unicode(opts.verbose_name)
        else:
            objects_name = force_unicode(opts.verbose_name_plural)

        title = _("Select symbol(s) that you want delete.")
        context = {
            "title": title,
            "objects_name": objects_name,
            'symbols': symbols,
            'queryset': queryset,
            "opts": opts,
            "app_label": app_label,
            'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
        }
        return TemplateResponse(request, [
            "admin/delete_symbol_confirmation.html"
        ], context, current_app=modeladmin.admin_site.name)
    delete_symbol.short_description =_('delete symbol')

    def get_readonly_fields(self, request, obj=None):
        if not tinycms_settings.PUBLISH_DEFAULT:
            if not request.user.has_perm('entries.publish_entry'):
                return ('publish',)

        return self.readonly_fields

class ArticleAdmin(EntryBaseAdmin):
    fieldsets = (
        (None, {
            'classes': ['extrapretty', 'article_base'],
            'fields': [('title', 'alternate_title'),
                       ('is_draft', 'publish'),
                       #('slug'),
                       ('jump'),
                       ('jump_to_url'),
                       ('category', 'source'),
                       ('meta_keywords'),
                       #('meta_keywords'),
                       ('thumbnail', 'alternate_thumbnail'),
                       ('description'),
                       ('content'),
                       ('symbol'),
                       ('titleclass'),
                       ('pub_date'),
                       ('allow_comment'),
                      ],
        }),
        (_('extra'), {
            'classes': ['collapse', 'extrapretty', 'article_content'],
            'fields': [('sub_category'),
                       ('template'),
                       ('meta_extra'),
                      ]
        }),
    )

    class Media:
        js = (
            'js/jquery.min.js',
            'js/tiny_mce/jquery.tinymce.js',
            'js/tiny_mce/tiny_mce.js',
            'js/colorbox/jquery.colorbox-min.js',
            'js/editor.js',
            'js/entry-actions.js',
        )
        css = {
            'all': ('js/colorbox/colorbox.css',
                    'js/swfupload/default.css',
            ),
        }

class VideoAdmin(EntryBaseAdmin):
    fieldsets = (
        (None, {
            'classes': ['extrapretty', 'video_base'],
            'fields': [('title', 'alternate_title'),
                       ('is_draft', 'publish'),
                       #('slug'),
                       ('jump'),
                       ('jump_to_url'),
                       ('category', 'source'),
                       ('meta_keywords'),
                       #('meta_keywords'),
                       ('thumbnail', 'alternate_thumbnail'),
                       ('description'),
                       ('video_url'),
                       ('symbol'),
                       ('titleclass'),
                       ('pub_date'),
                       ('allow_comment'),
                      ],
        }),
        (_('extra'), {
            'classes': ['collapse', 'extrapretty', 'article_content'],
            'fields': [('sub_category'),
                       ('template'),
                       ('meta_extra'),
                      ]
        }),
    )

    class Media:
        js = (
            'js/jquery.min.js',
            'js/entry-actions.js',
        )

admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Video, VideoAdmin)

# django floatpages
from django.contrib.flatpages.admin import FlatpageForm, FlatPageAdmin
from django.contrib.flatpages.models import FlatPage

class FlatPageExtendAdmin(FlatPageAdmin):

    class Media:
        js = (
            'js/jquery.min.js',
            'js/tiny_mce/jquery.tinymce.js',
            'js/tiny_mce/tiny_mce.js',
            'js/flatpages-editor.js',
            'js/colorbox/jquery.colorbox-min.js',
        )
        css = {
            'all': ('js/colorbox/colorbox.css',
                    'js/swfupload/default.css',
            ),
        }

admin.site.register(Symbol)
admin.site.register(TitleClass)
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageExtendAdmin)
