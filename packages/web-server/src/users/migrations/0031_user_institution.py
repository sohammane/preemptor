# Generated by Django 3.0.3 on 2020-12-30 17:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0003_auto_20201022_1926'),
        ('users', '0030_remove_user_is_professor'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='institution',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='institutions.Institution'),
        ),
    ]
