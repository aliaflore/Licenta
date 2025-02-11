# Generated by Django 5.0.6 on 2024-11-26 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('licenta', '0005_analysis_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysispdf',
            name='doctor_notes',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='analysispdf',
            name='suggestion',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='analysispdf',
            name='taken_on',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='radiographypdf',
            name='doctor_notes',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='radiographypdf',
            name='taken_on',
            field=models.DateField(null=True),
        ),
    ]
