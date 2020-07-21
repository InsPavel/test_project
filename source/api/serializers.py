from webapp.models import Article, Category
from rest_framework import serializers


class ArticleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title', 'category_id', 'user_id', 'description', 'image')


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'parent_id')
