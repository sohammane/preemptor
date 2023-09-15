# Generated by Django 3.0.3 on 2020-05-21 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('documents', '0004_document_assignment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('year', models.TextField()),
                ('authors', models.TextField()),
                ('journal', models.TextField()),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_updated', models.DateTimeField(auto_now=True)),
                ('documents', models.ManyToManyField(blank=True, related_name='references', to='documents.Document')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]