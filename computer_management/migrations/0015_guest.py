# Generated by Django 5.1.4 on 2025-02-07 02:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('computer_management', '0014_student_number_of_uses'),
    ]

    operations = [
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('guest_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('status', models.CharField(choices=[('A', 'Active'), ('I', 'Inactive'), ('D', 'Deleted')], default='Inactive', max_length=15)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('phone', models.CharField(max_length=20, null=True)),
                ('computer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='computer_management.computer', to_field='name')),
            ],
            options={
                'ordering': ['-updated', '-created'],
            },
        ),
    ]
