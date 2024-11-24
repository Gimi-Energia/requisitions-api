# Generated by Django 4.2.4 on 2024-07-10 19:52

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('maintenances', '0005_alter_maintenance_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Responsible',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('phone', models.CharField(max_length=15, verbose_name='Phone')),
                ('extension', models.CharField(max_length=10, verbose_name='Extension')),
            ],
        ),
    ]