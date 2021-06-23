from django.contrib import admin

from .models import Favourites, Follow, Ingredient, Purchase, Recipe, Tag


class IngredientRecipeInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'title')
    search_fields = ('author', 'title')
    list_filter = ('author', 'title', 'tags')
    inlines = (IngredientRecipeInline,)


class FavouritesAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit')
    list_filter = ('name',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Favourites, FavouritesAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
