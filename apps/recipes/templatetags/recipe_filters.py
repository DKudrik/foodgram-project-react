from django import template
from apps.recipes.models import Favourites, Follow, Purchase, Tag

register = template.Library()


@register.filter
def counter(author):
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
    return Follow.objects.filter(author=author, user=user).exists()


@register.filter
def in_favorites(user, recipe):
    return Favourites.objects.filter(user=user, recipe=recipe).exists()


@register.filter
def in_purchases(user, recipe):
    return Purchase.objects.filter(user=user, recipe=recipe).exists()


@register.filter
def get_filter_tags(request, tag):
    new_request = request.GET.copy()
    all_tags = Tag.objects.all()
    tags_list = request.GET.getlist('tags')
    print('tag: ', tag)
    if not tags_list:
        for tag in all_tags:
            tags_list.append(tag.name)
        new_request.setlist('tags', tags_list)
        print(1111)
        return new_request.urlencode()
    else:
        tags_list = new_request.getlist('tags')
    if tag.name in tags_list:
        print(tags_list)
        print(tag.name)
        tags_list.remove(tag.name)
        print(tags_list)
        new_request.setlist('tags', tags_list)
        print('if')
    else:
        new_request.appendlist('tags', tag)
        print('else')
    print('tag_list: ', tags_list)
    return new_request.urlencode()
