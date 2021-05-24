from django import forms
from django.contrib.auth import get_user_model
from django.db import models
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import Recipe


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = [
            "title",
            "image",
            "description",
            "ingredients",
            "cooking_time",
        ]
        labels = {
            "group": _("Выберите группу(при необходимости)"),
        }
