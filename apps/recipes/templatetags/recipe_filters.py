from django import template
from apps.recipes.models import Tag

register = template.Library()


@register.filter
def counter(author):
    """Change a word declension depending on amount."""
    cnt = author.recipes.count()
    if cnt <= 3:
        return
    cnt -= 3
    if cnt % 10 in range(2, 5):
        return f'{cnt} рецепта'
    elif cnt in range(5, 21) or cnt % 10 in range(5, 10) or cnt % 10 == 0:
        return f'{cnt} рецептов'
    elif cnt % 10 == 1:
        return f'{cnt} рецепт'


@register.filter
def follow_exists(author, user):
    """Check subscription."""
    return author.following.filter(user=user).exists()


@register.filter
def in_favorites(user, recipe):
    """Check if a recipe is in favorites."""
    return recipe.favourites.filter(user=user).exists()


@register.filter
def in_purchases(user, recipe):
    """Check if a recipe is in purchases."""
    return recipe.purchases.filter(user=user).exists()


@register.filter
def get_filter_tags(request, choosen_tag):
    """
    Check incoming tag for sorting.
    In case there is not tag - all the tags are applied.
    """
    new_request = request.GET.copy()
    all_tags = Tag.objects.all()
    tags_list = request.GET.getlist('tags')
    if not tags_list:
        for tag in all_tags:
            tags_list.append(tag.name)
        if choosen_tag.name in tags_list:
            tags_list = set(tags_list)
            tags_list.remove(choosen_tag.name)
        new_request.setlist('tags', tags_list)
        return new_request.urlencode()
    if choosen_tag.name not in tags_list:
        tags_list.append(choosen_tag.name)
        new_request.setlist('tags', tags_list)
    else:
        tags_list = set(tags_list)
        tags_list.remove(choosen_tag.name)
        new_request.setlist('tags', tags_list)
    return new_request.urlencode()
