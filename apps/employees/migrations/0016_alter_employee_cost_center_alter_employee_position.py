# Generated by Django 4.2.4 on 2024-11-24 19:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('departments', '0002_remove_department_code_alter_department_id'),
        ('employees', '0015_alter_employee_cost_center'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='cost_center',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='departments.department'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='position',
            field=models.CharField(default='c1de8df7-c0f8-4c81-86c0-af2acd22fc73'),
            preserve_default=False,
        ),
    ]