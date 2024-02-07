# Generated by Django 4.2.4 on 2024-01-29 17:35

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('code', models.CharField(max_length=7, verbose_name='Code')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
            ],
        ),
    ]