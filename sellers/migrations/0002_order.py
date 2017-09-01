# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-01 10:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
        ('sellers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_items', models.IntegerField()),
                ('revenue', models.FloatField()),
                ('timestamp', models.DateField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sellers.Seller')),
            ],
        ),
    ]
