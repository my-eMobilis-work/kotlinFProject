# Generated by Django 5.1.3 on 2024-12-11 20:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twigaapp', '0004_rename_type_bookings_bookingtype_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookings',
            old_name='paid',
            new_name='mpesaRequestSent',
        ),
    ]