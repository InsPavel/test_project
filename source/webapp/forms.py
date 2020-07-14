from bootstrap_modal_forms.forms import BSModalModelForm
from django import forms
from webapp.models import Article, Category


class ArticleCreateForm(forms.ModelForm):
    def __init__(self, user=None, **kwargs):
        self.user = user
        if user and not user.is_authenticated:
            self.user = None
        super().__init__(**kwargs)

    def save(self, commit=True):
        self.instance.user_id = self.user
        return super().save(commit)

    class Meta:
        model = Article
        fields = ['category_id', 'title', 'description', 'image']


class CategoryForm(BSModalModelForm):
    class Meta:
        model = Category
        fields = ['title', 'parent_id']
