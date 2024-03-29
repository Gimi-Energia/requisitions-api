# Generated by Django 4.2.4 on 2024-02-09 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.CharField(max_length=6, primary_key=True, serialize=False, unique=True)),
                ('contract_number', models.CharField(max_length=10, verbose_name='Contract Number')),
                ('control_number', models.CharField(max_length=8, verbose_name='Control Number')),
                ('client_name', models.CharField(max_length=120, verbose_name='Client Name')),
                ('project_name', models.CharField(max_length=120, verbose_name='Client Name')),
                ('freight_value', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name='Freight Value')),
            ],
        ),
    ]
