from recipes.models import Ingredient
from django.core.management.base import BaseCommand

import csv


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('recipes/data/ingredients.csv') as file:
            file_reader = csv.reader(file)
            for row in file_reader:
                name, unit = row
                Ingredient.objects.get_or_create(name=name, unit=unit)
