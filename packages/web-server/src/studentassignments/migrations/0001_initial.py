# Generated by Django 3.0.3 on 2020-08-14 15:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assignments', '0006_auto_20200814_1435'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentAssignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.TextField(choices=[('O', 'Open'), ('I', 'In Progress'), ('R', 'In Revision'), ('G', 'Graded')], default='O', max_length=1)),
                ('grade', models.TextField(blank=True)),
                ('final_comment', models.TextField(blank=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_updated', models.DateTimeField(auto_now=True)),
                ('assignment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='assignments.Assignment')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
