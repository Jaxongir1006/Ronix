# Generated by Django 5.2 on 2025-04-25 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contactus',
            options={'ordering': ['-created_at'], 'verbose_name': 'Contact Us', 'verbose_name_plural': 'Contact Us'},
        ),
    ]
