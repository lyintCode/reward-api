# Generated by Django 5.2 on 2025-04-11 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rewards', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduledreward',
            name='execute_at',
            field=models.DateTimeField(db_index=True),
        ),
    ]
