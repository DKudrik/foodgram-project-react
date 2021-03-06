import csv

from django.core.management.base import BaseCommand

from apps.recipes.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('templates/ingredients/ingredients.csv') as file:
            file_reader = csv.reader(file)
            for row in file_reader:
                name, unit = row
                Ingredient.objects.get_or_create(name=name, unit=unit)
