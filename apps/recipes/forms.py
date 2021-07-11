from django import forms
from django.forms import ModelForm

from .models import Recipe, Tag


class RecipeForm(ModelForm):
    quantity = forms.DecimalField(min_value=0.1, decimal_places=2)

    class Meta:
        model = Recipe
        fields = [
            'title',
            'image',
            'description',
            'cooking_time',
            'tags'
        ]
        tags = forms.ModelMultipleChoiceField(
            queryset=Tag.objects.all(),
            widget=forms.CheckboxSelectMultiple
        )
