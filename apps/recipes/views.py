from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .forms import RecipeForm
from .models import (Favourites, Follow, Ingredient, IngredientRecipe,
                     Purchase, Recipe, Tag, User)
from .serializers import IngredientSerializer
from .utils import save_recipe, create_pdf
from django.conf import settings


def index(request):
    tags_list = request.GET.getlist('tags')
    if not tags_list:
        tags_list = ['завтрак', 'обед', 'ужин']
    all_tags = Tag.objects.all()
    recipes = Recipe.objects.filter(
        tags__name__in=tags_list
    ).select_related(
        'author'
    ).prefetch_related(
        'tags'
    ).distinct(
    ).order_by('-pk')
    paginator = Paginator(recipes, settings.PAGINATION_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'paginator': paginator,
               'recipe': recipes,
               'page': page,
               'all_tags': all_tags,
               'tags_list': tags_list}
    return render(request, 'index.html', context)


@login_required
def new_recipe(request):
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
    )
    if not form.is_valid():
        return render(request, 'recipes/new_recipe.html', {'form': form})
    save_recipe(request, form)
    return redirect('index')


def recipe_view(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'recipes/recipe.html', {
        'recipe': recipe,
    })


@login_required
def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    form = RecipeForm(request.POST or None,
                      files=request.FILES or None,
                      instance=recipe)
    if form.is_valid():
        edit_recipe(request, form, instance=recipe)
        return redirect('index')
    return render(request, 'recipes/new_recipe.html', {
        'form': form,
        'recipe_id': recipe_id,
        'recipe': recipe,
    })


def edit_recipe(request, form, instance):
    with transaction.atomic():
        IngredientRecipe.objects.filter(recipe=instance).delete()
        return save_recipe(request, form)


@login_required
def recipe_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if recipe.author != request.user:
        return redirect('recipe', username=request.user.username,
                        recipe_id=recipe_id)
    recipe.delete()
    return redirect('index')


@login_required
def profile(request, username):
    tags_list = request.GET.getlist('tags')
    if not tags_list:
        tags_list = ['завтрак', 'обед', 'ужин']
    all_tags = Tag.objects.all()
    recipes = Recipe.objects.filter(
        tags__name__in=tags_list, author__username=username
    ).select_related(
        'author'
    ).prefetch_related(
        'tags'
    ).distinct(
    ).order_by('-pk')
    author = get_object_or_404(User, username=username)
    paginator = Paginator(recipes, settings.PAGINATION_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'paginator': paginator,
               'recipes': recipes,
               'author': author,
               'page': page,
               'all_tags': all_tags,
               'tags_list': tags_list}
    return render(request, 'profile.html', context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if request.user != author:
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    follow_to_delete = get_object_or_404(Follow,
                                         user=request.user,
                                         author=author)
    follow_to_delete.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def profile_following(request, username):
    followings = User.objects.filter(
        following__user=request.user).all().order_by('-pk')
    paginator = Paginator(followings, settings.PAGINATION_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'myfollow.html', {
        'page': page,
        'paginator': paginator,
        'followings': followings,
    })


@api_view(('GET',))
def search_ingredients(request):
    text = request.GET.get('search', '')
    ingredients = Ingredient.objects.filter(
        name__istartswith=text)
    serializer = IngredientSerializer(ingredients, many=True)
    return Response(serializer.data)


@login_required
@api_view(['POST'])
def add_favorite(request):
    recipe = get_object_or_404(Recipe, id=request.data['id'])
    if Favourites.objects.filter(user=request.user, recipe=recipe).exists():
        return JsonResponse({'success': False})
    Favourites.objects.get_or_create(user=request.user, recipe=recipe)
    return JsonResponse({'success': True})


@login_required
@api_view(['DELETE'])
def remove_favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    favorite = Favourites.objects.filter(user=request.user, recipe=recipe)
    if favorite.exists():
        favorite.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
def profile_favorites(request, username):
    tags_list = request.GET.getlist('tags')
    if not tags_list:
        tags_list = ['завтрак', 'обед', 'ужин']
    all_tags = Tag.objects.all()
    recipes = Recipe.objects.filter(
        tags__name__in=tags_list, favourites__user__username=username
    ).select_related(
        'author'
    ).prefetch_related(
        'tags'
    ).distinct()
    paginator = Paginator(recipes, settings.PAGINATION_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'paginator': paginator,
               'recipes': recipes,
               'page': page,
               'all_tags': all_tags,
               'tags_list': tags_list}
    return render(request, 'favorite.html', context)


@login_required
@api_view(['POST'])
def add_purchase(request):
    recipe = get_object_or_404(Recipe, id=request.data['id'])
    if Purchase.objects.filter(user=request.user, recipe=recipe).exists():
        return JsonResponse({'success': False})
    Purchase.objects.get_or_create(user=request.user, recipe=recipe)
    return JsonResponse({'success': True})


@login_required
@api_view(['DELETE'])
def remove_purchase(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    purchase = Purchase.objects.filter(user=request.user, recipe=recipe)
    if purchase.exists():
        purchase.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
def remove_purchase_list(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    purchase = Purchase.objects.filter(user=request.user, recipe=recipe)
    purchase.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def profile_purchases(request, username):
    recipes = Recipe.objects.filter(purchases__user__username=username)
    paginator = Paginator(recipes, settings.PAGINATION_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'shopList.html', {
        'page': page,
        'paginator': paginator,
        'recipes': recipes,
    })


def purchases_download(request):
    return create_pdf(request)


def page_not_found(request, exception):
    return render(request, 'errors/404.html', {'path': request.path}, status=404)


def server_error(request):
    return render(request, 'errors/500.html', status=500)
