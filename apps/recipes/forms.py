from django import forms
from django.contrib.auth import get_user_model
from django.db import models
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import Comment, Post