# Generated by Django 4.2.4 on 2024-11-24 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0014_alter_employee_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='cost_center',
            field=models.CharField(default='c1de8df7-c0f8-4c81-86c0-af2acd22fc73'),
            preserve_default=False,
        ),
    ]