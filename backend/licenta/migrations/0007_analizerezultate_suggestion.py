# Generated by Django 5.0.6 on 2024-06-15 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('licenta', '0006_analize_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='analizerezultate',
            name='suggestion',
            field=models.TextField(null=True),
        ),
    ]