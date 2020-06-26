from django.contrib import admin
from webapp.models import Article, Category


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user_id']
    list_filter = ['user_id']
    search_fields = ['title', 'user_id']


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
