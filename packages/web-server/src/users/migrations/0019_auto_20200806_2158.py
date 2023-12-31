# Generated by Django 3.0.3 on 2020-08-06 21:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_auto_20200731_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='voucher',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='UserExperience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.TextField(choices=[('E', 'Education'), ('W', 'Work')], default=('E', 'Education'), max_length=1)),
                ('name', models.TextField(blank=True)),
                ('subname', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('date_start', models.DateField()),
                ('date_end', models.DateField(blank=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
