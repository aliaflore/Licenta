# Generated by Django 5.0.6 on 2025-02-01 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('licenta', '0020_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='doctor_proof',
            field=models.FileField(blank=True, null=True, upload_to='doctor-proofs/'),
        ),
    ]
