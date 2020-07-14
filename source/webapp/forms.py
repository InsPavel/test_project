from django import forms
from webapp.models import Article


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
