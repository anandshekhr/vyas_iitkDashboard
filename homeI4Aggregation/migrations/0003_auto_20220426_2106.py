# Generated by Django 3.2.13 on 2022-04-26 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homeI4Aggregation', '0002_componentdetails_hmidetail_inhouseinventory_machinedetails_operationsdetails'),
    ]

    operations = [
        migrations.RenameField(
            model_name='machinedetails',
            old_name='Manufacturer',
            new_name='line',
        ),
        migrations.RenameField(
            model_name='machinedetails',
            old_name='remarks',
            new_name='operation',
        ),
        migrations.RenameField(
            model_name='machinedetails',
            old_name='shopName',
            new_name='status',
        ),
    ]
