# Generated by Django 3.0.3 on 2020-08-17 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0006_document_studentassignment'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='requires_face',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='document',
            name='requires_voice',
            field=models.BooleanField(default=False),
        ),
    ]
