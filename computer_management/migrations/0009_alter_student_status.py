# Generated by Django 5.1.4 on 2025-01-15 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('computer_management', '0008_alter_student_options_student_option'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='status',
            field=models.CharField(choices=[('A', 'Active'), ('I', 'Inactive'), ('D', 'Deleted')], default='Inactive', max_length=15),
        ),
    ]
