# Generated by Django 4.2.4 on 2024-01-31 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('departments', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name='code',
        ),
        migrations.AlterField(
            model_name='department',
            name='id',
            field=models.CharField(max_length=7, primary_key=True, serialize=False, unique=True),
        ),
    ]