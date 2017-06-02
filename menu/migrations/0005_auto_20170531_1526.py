# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-31 19:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0004_auto_20170530_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='ingredients',
            field=models.ManyToManyField(related_name='ingredients', to='menu.Ingredient'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='expiration_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]