# Generated by Django 3.0.3 on 2021-03-11 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0005_institution_msg_1000_merits'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institution',
            name='msg_auth_good_1',
            field=models.TextField(blank=True, default="Great job! I'm glad to see you are doing your own work!<br/><br/>You're on the right track!<br/><br/>Congratulations!"),
        ),
        migrations.AlterField(
            model_name='institution',
            name='msg_auth_good_after_bad',
            field=models.TextField(blank=True, default='We can see how hard you are working to complete this task. Keep up the great work.'),
        ),
    ]