# Generated by Django 4.2.4 on 2024-12-03 21:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0012_alter_purchase_motive'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='purchaseproduct',
            unique_together=set(),
        ),
    ]