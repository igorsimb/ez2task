from django.contrib import admin
from django.contrib.admin import display

from .models import Item, Category, Comment

class CustomItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'get_author_company', 'date_posted')
    list_editable = ('date_posted',)

    @display(ordering='author__company', description='Author Company')
    def get_author_company(self, obj):
        return obj.author.company


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'date_posted', 'is_published')
    search_fields = ('user__username', 'item__title',)
    list_editable = ('is_published',)
    list_filter = ('is_published', 'date_posted')

admin.site.register(Item, CustomItemAdmin)
admin.site.register(Category)
admin.site.register(Comment, CommentAdmin)
