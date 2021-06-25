from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator


User = get_user_model()


class Tag(models.Model):
    """Describes a tag object."""
    name = models.CharField(max_length=255, verbose_name='Имя')
    color = models.CharField(max_length=100, blank=True,
                             verbose_name='Цвет', default='')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Describes an ingredient object."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название',
    )
    unit = models.CharField(
        max_length=64,
        verbose_name='Ед. измерения',
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.unit}'


class Recipe(models.Model):
    """
    Describes a recipe object. Related to 'auth.User', 'recipe.Tag' and
    'recipe.Ingredient' through intermediate model 'IngredientRecipe'.
    """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    title = models.CharField(
        max_length=256,
        blank=False,
        verbose_name='Название',
    )
    image = models.ImageField(
        upload_to='kartinki/',
        blank=False,
        null=True,
        verbose_name='Изображение',
    )
    description = models.TextField(
        blank=False,
        verbose_name='Описание',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        related_name='recipes',
        verbose_name='Ингредиенты',
    )
    cooking_time = models.PositiveIntegerField(
        blank=False,
        verbose_name='Время приготовления, мин',
        validators=[MinValueValidator(1)]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги',
    )
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return (f'{self.author} : {self.title}')


class IngredientRecipe(models.Model):
    """
    Serves to connect a recipe oиject with an ingredient object
    via Many2Many relationship. Adds an additional field 'quantity'.
    """
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   related_name='ingredientrecipe',
                                   verbose_name='Ингредиент')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='ingredientrecipe',
                               verbose_name='Ингредиент')
    quantity = models.DecimalField(
        max_digits=8,
        decimal_places=1,
        verbose_name='Количество',
        validators=[MinValueValidator(0.1)]
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'

    def __str__(self):
        return (self.ingredient.name)


class Follow(models.Model):
    """Describes a follow object."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='user_author'
            )
        ]
        ordering = ('author', )
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return (f'Подписчик: {self.user}, Автор: {self.author}')


class Purchase(models.Model):
    """Describes a purchase object."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='purchases',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='purchases',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_purchase'
            )
        ]

    def __str__(self):
        return (f'Пользователь: {self.user}, Рецепт: {self.recipe}')


class Favourite(models.Model):
    """Describes a user's favourite recipes."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favourites',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favourites',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favourite'
            )
        ]

    def __str__(self):
        return (f'Пользователь: {self.user}, Рецепт: {self.recipe}')
