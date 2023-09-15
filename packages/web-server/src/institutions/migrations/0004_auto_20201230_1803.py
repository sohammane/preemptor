# Generated by Django 3.0.3 on 2020-12-30 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0003_auto_20201022_1926'),
    ]

    operations = [
        migrations.AddField(
            model_name='institution',
            name='msg_auth_bad_1',
            field=models.TextField(blank=True, default='Did you know that it’s important to do your own work, use your own words?<br/><br/>Did you know that employers/recruiters care about writing skills and critical thinking (your own thoughts)?<br/><br/>To collect more points, be an original, by using your own words!'),
        ),
        migrations.AddField(
            model_name='institution',
            name='msg_auth_bad_2',
            field=models.TextField(blank=True, default='We see a second case of plagiarism or impersonation in your work. We recommend you:<br/>1. Contact Library<br/>2. Contact Student Academic Supports<br/>3. Reach out to your faculty/ tutor on how to correct this.<br/><br/>Remember, we are here to help you be successful. When you do your own work, you get marks and you gain a competitive advantage.<br/><br/>Getting the help, you need will reduce the risk of being placed on academic probation or expelled!'),
        ),
        migrations.AddField(
            model_name='institution',
            name='msg_auth_bad_3',
            field=models.TextField(blank=True, default='It looks like you are still having some problems with your assignment. The Centre for Academic English and Library are here to help you avoid these problems and to help you gain confidence in your writing originality. Please click here to book an appointment and get support.'),
        ),
        migrations.AddField(
            model_name='institution',
            name='msg_auth_good_1',
            field=models.TextField(blank=True, default="Great job! I'm glad to see you are doing your own work!<br/><br/>You're on the right track!<br/><br/>Congratulations. you have earned 10 points!"),
        ),
        migrations.AddField(
            model_name='institution',
            name='msg_auth_good_after_bad',
            field=models.TextField(blank=True, default='We can see how hard you are working to complete this task. To recognize this hard work, we will give you 20 more points. Keep up the great work.'),
        ),
        migrations.AddField(
            model_name='institution',
            name='msg_copy_paste',
            field=models.TextField(blank=True, default='We see copy and pasting here. Take the time to use your own words. You can do this learning to have confidence in your own writing takes time. Cutting and pasting can cost you a lot in your studied and when you enter the work force! Originality is a foundation for success so start writing on your own now to be more prepared for the job market.'),
        ),
    ]
