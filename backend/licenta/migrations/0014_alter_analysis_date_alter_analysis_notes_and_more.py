# Generated by Django 5.0.6 on 2025-01-09 12:30

import encrypted_model_fields.fields
import licenta.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('licenta', '0013_alter_analysisprovider_analysis_columns'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analysis',
            name='date',
            field=encrypted_model_fields.fields.EncryptedDateField(null=True),
        ),
        migrations.AlterField(
            model_name='analysis',
            name='notes',
            field=encrypted_model_fields.fields.EncryptedTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='analysispdf',
            name='doctor_notes',
            field=encrypted_model_fields.fields.EncryptedTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='analysispdf',
            name='suggestion',
            field=encrypted_model_fields.fields.EncryptedTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='analysispdf',
            name='taken_on',
            field=encrypted_model_fields.fields.EncryptedDateField(null=True),
        ),
        migrations.AlterField(
            model_name='analysisresult',
            name='doctor_note',
            field=encrypted_model_fields.fields.EncryptedTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='analysisresult',
            name='in_range',
            field=encrypted_model_fields.fields.EncryptedBooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='analysisresult',
            name='measurement_unit',
            field=encrypted_model_fields.fields.EncryptedTextField(),
        ),
        migrations.AlterField(
            model_name='analysisresult',
            name='name',
            field=encrypted_model_fields.fields.EncryptedTextField(),
        ),
        migrations.AlterField(
            model_name='analysisresult',
            name='range_max',
            field=licenta.models.EncryptedDecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='analysisresult',
            name='range_min',
            field=licenta.models.EncryptedDecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='analysisresult',
            name='refference_range',
            field=encrypted_model_fields.fields.EncryptedTextField(),
        ),
        migrations.AlterField(
            model_name='analysisresult',
            name='result',
            field=encrypted_model_fields.fields.EncryptedTextField(),
        ),
        migrations.AlterField(
            model_name='analysisresult',
            name='suggestion',
            field=encrypted_model_fields.fields.EncryptedTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='radiographypdf',
            name='doctor_notes',
            field=encrypted_model_fields.fields.EncryptedTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='radiographypdf',
            name='taken_on',
            field=encrypted_model_fields.fields.EncryptedDateField(null=True),
        ),
    ]
