# Generated by Django 5.1.4 on 2025-01-18 15:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('computer_management', '0009_alter_student_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': ['-updated', 'created']},
        ),
        migrations.AddField(
            model_name='computer',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='computer',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='student_history',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('history_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(max_length=765, null=True)),
                ('title', models.CharField(max_length=255, null=True)),
                ('computer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='computer_management.computer', to_field='name')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='computer_management.student', to_field='code')),
            ],
            options={
                'ordering': ['-end_date'],
            },
        ),
    ]
