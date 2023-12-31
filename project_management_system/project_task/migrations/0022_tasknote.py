# Generated by Django 4.2.3 on 2023-08-05 08:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_task', '0021_alter_employee_profile_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField()),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_task.task')),
            ],
        ),
    ]
