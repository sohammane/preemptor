# Generated by Django 3.0.3 on 2020-05-08 18:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0001_initial'),
        ('documents', '0003_document_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='assignment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='assignments.Assignment'),
        ),
    ]
