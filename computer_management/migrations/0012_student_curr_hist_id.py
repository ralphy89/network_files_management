# Generated by Django 5.1.4 on 2025-01-19 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('computer_management', '0011_alter_student_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='curr_hist_id',
            field=models.BigIntegerField(null=True),
        ),
    ]
