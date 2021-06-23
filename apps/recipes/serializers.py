from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Favourites, Follow, Ingredient, Purchase


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['name', 'unit']
        model = Ingredient


class FavouritesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Favourites
        validators = [
            UniqueTogetherValidator(
                queryset=Favourites.objects.all(),
                fields=['user', 'recipe']
            )
        ]


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Purchase
        validators = [
            UniqueTogetherValidator(
                queryset=Purchase.objects.all(),
                fields=['user', 'recipe']
            )
        ]


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'author']
            )
        ]
