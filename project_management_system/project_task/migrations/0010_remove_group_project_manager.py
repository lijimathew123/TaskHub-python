# Generated by Django 4.2.3 on 2023-07-17 10:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_task', '0009_group_project_manager'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='project_manager',
        ),
    ]
