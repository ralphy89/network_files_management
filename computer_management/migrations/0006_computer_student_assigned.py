# Generated by Django 5.1.4 on 2025-01-12 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('computer_management', '0005_remove_student_assigned_computers_student_computer'),
    ]

    operations = [
        migrations.AddField(
            model_name='computer',
            name='student_assigned',
            field=models.JSONField(null=True),
        ),
    ]
