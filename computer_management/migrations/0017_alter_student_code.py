# Generated by Django 5.1.4 on 2025-02-07 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('computer_management', '0016_student_phone_student_type_alter_student_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='code',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
    ]
