# Generated by Django 5.2 on 2025-04-25 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='branch',
            options={'verbose_name': 'Branch', 'verbose_name_plural': 'Branches'},
        ),
        migrations.AlterModelOptions(
            name='branchtranslation',
            options={'default_permissions': (), 'managed': True, 'verbose_name': 'Branch Translation'},
        ),
        migrations.AddField(
            model_name='branch',
            name='email',
            field=models.EmailField(blank=True, max_length=200, null=True, verbose_name='Branch email'),
        ),
    ]
