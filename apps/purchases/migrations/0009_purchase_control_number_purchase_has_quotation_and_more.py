# Generated by Django 4.2.4 on 2024-04-16 13:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('purchases', '0008_alter_purchase_status_alter_purchaseproduct_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='control_number',
            field=models.IntegerField(default=0, verbose_name='Control Number'),
        ),
        migrations.AddField(
            model_name='purchase',
            name='has_quotation',
            field=models.BooleanField(default=True, verbose_name='Has Quotation?'),
        ),
        migrations.AddField(
            model_name='purchase',
            name='quotation_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Quotation Date'),
        ),
        migrations.AddField(
            model_name='purchase',
            name='quotation_emails',
            field=models.TextField(blank=True, null=True, verbose_name='Purchase Quotation Emails'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='approver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Approver', to=settings.AUTH_USER_MODEL, verbose_name='Approver'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='status',
            field=models.CharField(choices=[('Opened', 'Opened'), ('Approved', 'Approved'), ('Denied', 'Denied'), ('Canceled', 'Canceled'), ('Quotation', 'Quotation')], default='Opened', max_length=9, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='purchaseproduct',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Price'),
        ),
        migrations.AlterField(
            model_name='purchaseproduct',
            name='status',
            field=models.CharField(choices=[('Opened', 'Opened'), ('Approved', 'Approved'), ('Denied', 'Denied'), ('Canceled', 'Canceled'), ('Quotation', 'Quotation')], default='Opened', max_length=9, verbose_name='Status'),
        ),
    ]
