# Generated by Django 4.2.4 on 2024-12-03 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0013_alter_purchaseproduct_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseproduct',
            name='obs',
            field=models.TextField(blank=True, null=True, verbose_name='Observation'),
        ),
    ]