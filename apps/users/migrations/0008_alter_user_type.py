# Generated by Django 4.2.4 on 2024-05-01 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='type',
            field=models.CharField(choices=[('Requester', 'Requester'), ('Approver', 'Approver'), ('Director', 'Director'), ('Admin', 'Admin')], default='Requester', max_length=9, verbose_name='Type'),
        ),
    ]
