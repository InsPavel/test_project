from bootstrap_modal_forms.forms import BSModalModelForm
from django import forms
from webapp.models import Article, Category


class ArticleCreateForm(forms.ModelForm):
    def __init__(self, user=None, **kwargs):
        self.user = user
        super().__init__(**kwargs)

    def save(self, commit=True):
        self.instance.user_id = self.user
        return super().save(commit)

    class Meta:
        model = Article
        fields = ['category_id', 'title', 'description', 'image']


class CategoryForm(BSModalModelForm):
    def clean_title(self):
        title = self.cleaned_data.get('title')
        category = Category.objects.filter(title=title)
        if len(category) != 0:
            raise forms.ValidationError('Данная категория уже существует!')
        return title

    class Meta:
        model = Category
        fields = ['title', 'parent_id']
