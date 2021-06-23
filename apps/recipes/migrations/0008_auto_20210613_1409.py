# Generated by Django 2.2.19 on 2021-06-13 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_remove_tag_style'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='value',
        ),
        migrations.AddField(
            model_name='tag',
            name='color',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='tagcolor'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(default='qwerty', max_length=255, verbose_name='tagname'),
            preserve_default=False,
        ),
    ]