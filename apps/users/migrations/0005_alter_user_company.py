# Generated by Django 4.2.4 on 2024-02-09 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='company',
            field=models.CharField(choices=[('Gimi', 'Gimi'), ('GBL', 'GBL'), ('GPB', 'GPB'), ('Group', 'Group')], default='Gimi', max_length=5, verbose_name='Company'),
        ),
    ]
