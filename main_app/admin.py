from django.contrib import admin
from django.contrib.admin import display

from .models import Item, Category, Comment

class CustomItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'get_author_company', 'date_posted')
    list_editable = ('date_posted',)
    readonly_fields = ('id',)

    @display(ordering='author__company', description='Author Company')
    def get_author_company(self, obj):
        return obj.author.company


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'date_posted', 'is_published')
    search_fields = ('user__username', 'item__title',)
    list_editable = ('is_published',)
    list_filter = ('is_published', 'date_posted')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_title', 'get_category_company', 'category_author')


    @display(ordering='category_author__company')
    def get_category_company(self, obj):
        return obj.category_author.company

admin.site.register(Item, CustomItemAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
