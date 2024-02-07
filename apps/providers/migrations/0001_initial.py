# Generated by Django 4.2.4 on 2024-02-07 18:34

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('cnpj', models.CharField(max_length=14, verbose_name='CNPJ')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('phone', models.EmailField(blank=True, max_length=11, null=True, verbose_name='Phone')),
            ],
        ),
    ]