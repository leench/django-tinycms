try:
    import json
except ImportError:
    from django.utils import simplejson as json

from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from mptt.admin import MPTTModelAdmin

from models import Category

class CategoryAdmin(MPTTModelAdmin):
    list_display = ('pk', 'name', 'get_absolute_url_link', 'tree_id', 'lft', 'rght', 'level', 'parent', 'slug', 'active', 'create_date')
    list_display_links = ('name', )

    def get_absolute_url_link(self, obj):
        u = '<a href="../../r/%s/%s/" target="_blank">%s</a>' % (ContentType.objects.get(model="category").id, obj.id, obj.get_absolute_url())
        return mark_safe(u)
    get_absolute_url_link.short_description = _('absolute url')
    get_absolute_url_link.allow_tags = True

admin.site.register(Category, CategoryAdmin)
