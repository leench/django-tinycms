from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from tinycms.commentmod import CommentMod
from tinycms.commentmod.models import Reply

class ReplyAdmin(admin.TabularInline):
    model = Reply
    extra = 1

class CommentModAdmin(admin.ModelAdmin):
    list_display = ('get_user_name', 'is_public', 'user_email', 'comment', 'submit_date')
    ordering = ('-submit_date',)
    actions = ['public', 'unpublic']
    inlines = [ReplyAdmin, ]

    def get_user_name(self, obj):
        if obj.user_name:
            return obj.user_name
        else:
            return _('anonymous')

    def public(modeladmin, request, queryset):
        queryset.update(is_public=True)
    public.short_description = _('public')

    def unpublic(modeladmin, request, queryset):
        queryset.update(is_public=False)
    unpublic.short_description =  _('unpublic')

    fieldsets = (
        (None, {
            'fields': ('user_name', 'user_email', 'phone', 'is_public', 'comment', 'submit_date', 'ip_address', 'is_removed')
        }),
    )

admin.site.register(CommentMod, CommentModAdmin)
