from django.contrib import admin

from .models import Ingredient, IngredientRecipe, Recipe


class IngredientRecipeInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientRecipeInline, )


admin.site.register(Ingredient)
admin.site.register(IngredientRecipe)
admin.site.register(Recipe, RecipeAdmin)
