# Generated by Django 4.2.3 on 2023-07-26 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_task', '0016_employee_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='domain',
            field=models.CharField(blank=True, choices=[('Designer', 'Designer'), ('Developer', 'Developer'), ('Tester', 'Tester'), ('Client Communication', 'Client Communication')], max_length=20, null=True),
        ),
    ]
