# Generated by Django 4.2.4 on 2024-09-13 18:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("purchases", "0011_alter_purchaseproduct_quantity"),
    ]

    operations = [
        migrations.AlterField(
            model_name="purchase",
            name="motive",
            field=models.TextField(verbose_name="Motive"),
        ),
    ]
