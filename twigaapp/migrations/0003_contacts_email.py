# Generated by Django 5.1.3 on 2024-12-10 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twigaapp', '0002_delete_managernotes'),
    ]

    operations = [
        migrations.AddField(
            model_name='contacts',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
