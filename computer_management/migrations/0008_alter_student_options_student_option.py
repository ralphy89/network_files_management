# Generated by Django 5.1.4 on 2025-01-15 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('computer_management', '0007_alter_student_computer'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': ['-student_id']},
        ),
        migrations.AddField(
            model_name='student',
            name='option',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
