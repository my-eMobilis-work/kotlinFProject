# Generated by Django 5.1.3 on 2024-12-11 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twigaapp', '0003_contacts_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookings',
            old_name='type',
            new_name='bookingType',
        ),
        migrations.RenameField(
            model_name='bookings',
            old_name='dateTime',
            new_name='dateBooked',
        ),
        migrations.RenameField(
            model_name='bookings',
            old_name='booking_time',
            new_name='dateCreated',
        ),
        migrations.AlterField(
            model_name='bookings',
            name='name',
            field=models.CharField(max_length=70),
        ),
        migrations.AlterField(
            model_name='bookings',
            name='persons',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='bookings',
            name='phone',
            field=models.CharField(max_length=15),
        ),
    ]
