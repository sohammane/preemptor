# Generated by Django 3.0.3 on 2020-08-14 14:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assignments', '0005_auto_20200813_1949'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='grade',
        ),
        migrations.AlterField(
            model_name='assignment',
            name='status',
            field=models.TextField(choices=[('D', 'Draft'), ('O', 'Open'), ('I', 'In Progress'), ('C', 'Closed')], default='D', max_length=1),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
