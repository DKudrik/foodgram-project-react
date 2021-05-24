from django.contrib.auth import get_user_model
from django.db import models
from taggit.managers import TaggableManager

User = get_user_model()


class Ingredient(models.Model):
    """Describes an ingredient object."""
    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    name = models.CharField(
        max_length=256,
        verbose_name='Название',
    )
    unit = models.CharField(
        max_length=64,
        verbose_name='Ед. измерения',
    )

    def __str__(self):
        return f'{self.name}, {self.unit}'


class Tag(models.Model):
    pass


class Recipe(models.Model):
    """
    Describes a recipe object. Related to 'auth.User', 'recipes.Tag' and
    'recipes.Ingredient' through intermediate model 'recipes.IngredientRecipe'.
    """
    class Meta:
        ordering = ("-pub_date", )
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор",
    )
    title = models.CharField(
        max_length=256,
        blank=False,
        verbose_name="Название",
    )
    image = models.ImageField(
        upload_to="kartinki/",
        blank=True,
        null=True,
        verbose_name="Изображение",
    )
    description = models.TextField(
        blank=False,
        verbose_name="Описание",
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        related_name='ingredients',
        verbose_name='Ингредиенты',
    )
    cooking_time = models.IntegerField(
        blank=False,
        verbose_name='Время приготовления, мин',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации",
    )

    def __str__(self):
        return self.title


class IngredientRecipe(models.Model):
    """
    Serves to connect a recipe oject with an ingredient object
    via Many2Many relationship. Add an additional field 'quantity'.
    """
    class Meta:
        verbose_name = "Ингредиент в рецепте"
        verbose_name_plural = "Ингредиенты в рецепте"

    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    quantity = models.DecimalField(
        max_digits=6,
        decimal_places=1,
        verbose_name='Количество',
    )

    def __str__(self):
        return 'Ингредиент'
