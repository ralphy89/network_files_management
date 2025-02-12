# Generated by Django 5.1.4 on 2025-02-07 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('computer_management', '0015_guest'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='phone',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='type',
            field=models.CharField(choices=[('S', 'Student'), ('G', 'Guest')], default='Student', max_length=100),
        ),
        migrations.AlterField(
            model_name='student',
            name='code',
            field=models.CharField(max_length=20, null=True, unique=True),
        ),
        migrations.DeleteModel(
            name='Guest',
        ),
    ]
