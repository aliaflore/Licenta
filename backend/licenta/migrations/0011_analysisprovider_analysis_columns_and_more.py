# Generated by Django 5.0.6 on 2024-11-26 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('licenta', '0010_analysisprovider_analysis_providedlang'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysisprovider',
            name='analysis_columns',
            field=models.JSONField(default=[0, 1, 2, 3]),
        ),
        migrations.AddField(
            model_name='analysisprovider',
            name='analysis_list_skip_first_row',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='analysisprovider',
            name='analysis_list_skip_first_table',
            field=models.BooleanField(default=False),
        ),
    ]
