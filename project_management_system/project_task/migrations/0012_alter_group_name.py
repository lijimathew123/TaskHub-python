# Generated by Django 4.2.3 on 2023-07-19 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_task', '0011_group_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
    ]
