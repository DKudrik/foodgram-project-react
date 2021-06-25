import io
from decimal import Decimal

import reportlab
from django.conf import settings
from django.db import transaction
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from reportlab.lib.colors import (black, green, grey, lightgrey, orange,
                                  purple, white)
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from .models import Ingredient, IngredientRecipe, Recipe, Tag

reportlab.rl_config.TTFSearchPath.append(
    str(settings.BASE_DIR) + '/assets/reportlabs/fonts')


TAGG_LIST = ['завтрак', 'обед', 'ужин']


def get_ingredients(request):
    """Get ingredients from POST request and search them in DB."""
    ingredients = {}
    post = request.POST
    for key, name in post.items():
        if key.startswith('nameIngredient'):
            num = key.partition('_')[-1]
            ingredients[name] = post[f'valueIngredient_{num}']
    return ingredients


def get_tags(request):
    TAGS = {
        'breakfast': 'завтрак',
        'lunch': 'обед',
        'dinner': 'ужин'
    }
    tags = []
    post = request.POST
    for key, name in post.items():
        if key in TAGS and name == 'on':
            tags.append(Tag.objects.get(name=TAGS[key]))
    return tags


def create_tags_list(request):
    tags_list = request.GET.getlist('tags')
    if not tags_list:
        tags_list = TAGG_LIST
    return tags_list


def save_recipe(request, form):
    with transaction.atomic():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()
        tags = get_tags(request)
        for tag in tags:
            recipe.tags.add(tag)
        objs = []
        ingredients = get_ingredients(request)
        for name, quantity in ingredients.items():
            ingredient = get_object_or_404(Ingredient, name=name)
            objs.append(
                IngredientRecipe(
                    recipe=recipe,
                    ingredient=ingredient,
                    quantity=Decimal(quantity.replace(',', '.'))
                )
            )
        IngredientRecipe.objects.bulk_create(objs)
        form.save_m2m()
        return recipe


def edit_recipe(request, form, instance):
    with transaction.atomic():
        IngredientRecipe.objects.filter(recipe=instance).delete()
        return save_recipe(request, form)


def collect_purchases_ingredients(request):
    """Collect ingredients from recipes in purchases and add them in a dict."""
    if request.user.is_authenticated:
        recipes = Recipe.objects.filter(
            purchases__user=request.user)
    else:
        user_ip = request.META['REMOTE_ADDR']
        recipe_pks = []
        if request.session.get(user_ip):
            recipe_pks = request.session[user_ip]
            recipes = Recipe.objects.filter(pk__in=recipe_pks)
    shoplist = {}
    for recipe in recipes:
        ingredients = recipe.ingredients.values_list('name', 'unit')
        amount = recipe.ingredientrecipe.values_list('quantity', flat=True)
        for num in range(len(ingredients)):
            title = ingredients[num][0]
            unit = ingredients[num][1]
            quantity = amount[num]
            if title in shoplist:
                shoplist[title] = [shoplist[title][0] + quantity, unit]
            else:
                shoplist[title] = [quantity, unit]
    return shoplist


def add_grapichs(pdf, font_size):
    """Add logo and horizontal stripes for better reading."""
    pdf.setFont('Vlashu', 20)
    pdf.setFillColor(orange)
    pdf.circle(150*mm, 8*mm, 3*mm, fill=1)
    pdf.setFillColor(green)
    pdf.circle(155*mm, 8*mm, 3*mm, fill=1)
    pdf.setFillColor(purple)
    pdf.circle(160*mm, 8*mm, 3*mm, fill=1)
    pdf.setFillColor(grey)
    pdf.drawString(165*mm, 10*mm, 'foodgram')
    y = 25*mm
    dy = font_size*mm
    for i in range(100):
        for color in (lightgrey, white):
            pdf.setFillColor(color)
            pdf.rect(0, y, 210*mm, dy, stroke=0, fill=1)
            y += dy
    pdf.setFillColor(white)
    pdf.rect(0, 275*mm, 210*mm, 297*mm, stroke=0, fill=1)
    y += dy


def create_pdf(request):
    shoplist = collect_purchases_ingredients(request)
    pdfmetrics.registerFont(TTFont('RussianPunk', 'RussianPunk.ttf'))
    pdfmetrics.registerFont(TTFont('Vlashu', 'Vlashu.otf'))
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)
    font_size = 6
    add_grapichs(pdf, font_size)
    pdf.setFont('RussianPunk', font_size*mm)
    x = 15*mm
    y = 25*mm
    pdf.setFillColor(black)
    for key in shoplist:
        pdf.drawString(x, y, key)
        x += 320
        pdf.drawString(x, y, str(shoplist[key][0]))
        x += 60
        pdf.drawString(x, y, shoplist[key][1])
        x -= 380
        y += font_size*mm
        if y > 280*mm:
            y = 25*mm
            pdf.showPage()
            add_grapichs(pdf, font_size)
            pdf.setFillColor(black)
            pdf.setFont('RussianPunk', font_size*mm)
    pdf.setTitle('Shoplist')
    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='shoplist.pdf')
