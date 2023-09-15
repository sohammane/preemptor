from django.db import models
from django.urls import reverse
from django_paranoid.models import ParanoidModel


class Institution(ParanoidModel):
    #  Fields
    name = models.TextField(blank=True)

    msg_auth_good_1 = models.TextField(
        blank=True,
        default="Great job! I'm glad to see you are doing your own work!<br/><br/>You're on the right track!<br/><br/>Congratulations!",
    )
    msg_auth_bad_1 = models.TextField(
        blank=True,
        default="Did you know that it’s important to do your own work, use your own words?<br/><br/>Did you know that employers/recruiters care about writing skills and critical thinking (your own thoughts)?<br/><br/>To collect more points, be an original, by using your own words!",
    )
    msg_auth_bad_2 = models.TextField(
        blank=True,
        default="We see a second case of plagiarism or impersonation in your work. We recommend you:<br/>1. Contact Library<br/>2. Contact Student Academic Supports<br/>3. Reach out to your faculty/ tutor on how to correct this.<br/><br/>Remember, we are here to help you be successful. When you do your own work, you get marks and you gain a competitive advantage.<br/><br/>Getting the help, you need will reduce the risk of being placed on academic probation or expelled!",
    )
    msg_auth_bad_3 = models.TextField(
        blank=True,
        default="It looks like you are still having some problems with your assignment. The Centre for Academic English and Library are here to help you avoid these problems and to help you gain confidence in your writing originality. Please click here to book an appointment and get support.",
    )
    msg_auth_good_after_bad = models.TextField(
        blank=True,
        default="We can see how hard you are working to complete this task. Keep up the great work.",
    )
    msg_copy_paste = models.TextField(
        blank=True,
        default="We see copy and pasting here. Take the time to use your own words. You can do this learning to have confidence in your own writing takes time. Cutting and pasting can cost you a lot in your studied and when you enter the work force! Originality is a foundation for success so start writing on your own now to be more prepared for the job market.",
    )
    msg_1000_merits = models.TextField(
        blank=True,
        default="Congratulations! You have earned 1000 points and have written an excellent amount of original work. You are doing well and are on the right track. Start thinking about how you’ll redeem your points!",
    )

    has_typing_cadence = models.BooleanField(default=True)
    has_facial_recognition = models.BooleanField(default=True)
    has_voice_recognition = models.BooleanField(default=True)
    has_screen_invigilation = models.BooleanField(default=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return str(self.pk)
