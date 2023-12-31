# Generated by Django 4.2.3 on 2023-07-31 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_task', '0018_employee_technologies_used'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')], max_length=100),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('Not Started', 'Not Started'), ('Start', 'Start'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], max_length=150),
        ),
    ]
