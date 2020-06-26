from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='categories')

    def __str__(self):
        return self.title


class Article(models.Model):
    category_id = models.ManyToManyField('webapp.Category', related_name='articles')
    user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(max_length=3000, verbose_name='Описание')
    image = models.ImageField(upload_to='article_image', null=True, blank=True, verbose_name='Картинка')
