from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from tinycms.commentmod import CommentMod
from tinycms.commentmod.models import Reply

class ReplyAdmin(admin.TabularInline):
    model = Reply
    extra = 1

class CommentModAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'is_public', 'user_email', 'comment', 'submit_date')
    ordering = ('-submit_date',)
    actions = ['public', 'unpublic']
    inlines = [ReplyAdmin, ]

    def publick(modeladmin, request, queryset):
        queryset.update(is_public=True)
    publick.short_description = _('public')

    def unpublic(modeladmin, request, queryset):
        queryset.update(is_public=False)
    unpublic.short_description =  _('unpublic')

    fieldsets = (
        (None, {
            'fields': ('user_name', 'user_email', 'phone', 'is_public', 'comment', 'submit_date')
        }),
    )

admin.site.register(CommentMod, CommentModAdmin)
