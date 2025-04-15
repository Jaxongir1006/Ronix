# Generated by Django 5.2 on 2025-04-13 08:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='category/')),
                ('name', models.CharField(max_length=200)),
                ('name_en', models.CharField(max_length=200, null=True)),
                ('name_uz', models.CharField(max_length=200, null=True)),
                ('name_ru', models.CharField(max_length=200, null=True)),
                ('description', models.TextField()),
                ('description_en', models.TextField(null=True)),
                ('description_uz', models.TextField(null=True)),
                ('description_ru', models.TextField(null=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Specification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
                ('size', models.CharField(max_length=100)),
                ('power', models.CharField(max_length=100)),
                ('voltage', models.CharField(max_length=100)),
                ('frequency', models.CharField(max_length=100)),
                ('speed', models.CharField(max_length=100)),
                ('capacity_wood', models.CharField(blank=True, max_length=100, null=True)),
                ('capacity_steel', models.CharField(blank=True, max_length=100, null=True)),
                ('weight', models.CharField(max_length=100)),
                ('supplied_in', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='products/', verbose_name='Image')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('name_en', models.CharField(max_length=200, null=True, verbose_name='Name')),
                ('name_uz', models.CharField(max_length=200, null=True, verbose_name='Name')),
                ('name_ru', models.CharField(max_length=200, null=True, verbose_name='Name')),
                ('model', models.CharField(max_length=100, verbose_name='Model')),
                ('features', models.TextField(verbose_name='Features')),
                ('features_en', models.TextField(null=True, verbose_name='Features')),
                ('features_uz', models.TextField(null=True, verbose_name='Features')),
                ('features_ru', models.TextField(null=True, verbose_name='Features')),
                ('description', models.TextField(verbose_name='Description')),
                ('description_en', models.TextField(null=True, verbose_name='Description')),
                ('description_uz', models.TextField(null=True, verbose_name='Description')),
                ('description_ru', models.TextField(null=True, verbose_name='Description')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.category')),
                ('specification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.specification')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
    ]
