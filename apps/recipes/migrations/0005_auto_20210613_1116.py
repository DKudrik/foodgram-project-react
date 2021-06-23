# Generated by Django 2.2.19 on 2021-06-13 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_recipe_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=50, null=True, verbose_name='Значение')),
                ('style', models.CharField(max_length=50, null=True, verbose_name='Стиль для шаблона')),
                ('name', models.CharField(max_length=50, null=True, verbose_name='Имя в шаблона')),
            ],
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='tag',
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(related_name='recipes', to='recipes.Tag'),
        ),
    ]