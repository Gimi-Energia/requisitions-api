# Generated by Django 4.2.4 on 2024-11-21 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0011_alter_purchaseproduct_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='company',
            field=models.CharField(choices=[('Gimi', 'Gimi'), ('GBL', 'GBL'), ('GPB', 'GPB'), ('GS', 'GS'), ('GIR', 'GIR'), ('Filial', 'Filial')], default='Gimi', max_length=6, verbose_name='Company'),
        ),
    ]
