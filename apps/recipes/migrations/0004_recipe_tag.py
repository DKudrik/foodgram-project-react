# Generated by Django 2.2.19 on 2021-06-13 07:37

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20210607_0649'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='tag',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Завтрак', 'Завтрак'), ('Обед', 'Обед'), ('Ужин', 'Ужин')], default='Обед', max_length=17, verbose_name='Теги'),
        ),
    ]
