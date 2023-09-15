from __future__ import unicode_literals
import random
import time
import os
from django_paranoid.models import ParanoidModel
from django.db import models
from django.core.mail import send_mail
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from .managers import UserManager

from institutions.models import Institution


def random_avatar_name(instance, filename):
    ext = filename.split(".")[-1]
    filename = "user_data/avatar_{}_{}.{}".format(
        time.time(), random.randint(0, 9999), ext
    )
    return filename


def random_cover_name(instance, filename):
    ext = filename.split(".")[-1]
    filename = "user_data/cover_{}_{}.{}".format(
        time.time(), random.randint(0, 9999), ext
    )
    return filename


class User(AbstractBaseUser, PermissionsMixin, models.Model):
    # Choices
    USER_ACADEMIC_LEVELS = (
        ("H", "High School"),
        ("C", "College"),
        ("M", "Master"),
        ("D", "Doctor"),
        ("O", "Other"),
    )
    ROLE_ADMIN = 1
    ROLE_PROFESSOR = 2
    ROLE_STUDENT = 3
    ROLE_SUPERVISOR = 4
    ROLES_CHOICES = (
        (ROLE_STUDENT, "Student"),
        (ROLE_PROFESSOR, "Professor"),
        (ROLE_ADMIN, "Admin"),
        (ROLE_SUPERVISOR, "Supervisor"),
    )

    #  Relationships
    institution = models.ForeignKey(
        Institution, on_delete=models.SET_NULL, blank=True, null=True
    )

    first_name = models.TextField(max_length=200, blank=True)
    last_name = models.TextField(max_length=200, blank=True)
    email = models.EmailField(unique=True)
    mobile = models.TextField(max_length=200, blank=True)
    student_number = models.TextField(max_length=200, blank=True)
    academic_level = models.TextField(
        max_length=1, choices=USER_ACADEMIC_LEVELS, default=USER_ACADEMIC_LEVELS[0][0],
    )
    other_academic_level = models.TextField(blank=True)
    university = models.TextField(max_length=200, blank=True)
    curriculum = models.TextField(max_length=200, blank=True)
    avatar = models.ImageField(upload_to=random_avatar_name, null=True, blank=True)
    cover = models.ImageField(upload_to=random_cover_name, null=True, blank=True)
    tdna_id = models.TextField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)

    role = models.PositiveSmallIntegerField(
        choices=ROLES_CHOICES, default=ROLE_STUDENT, null=True, blank=True
    )

    last_tdna_text = models.TextField(blank=True)

    has_typing = models.BooleanField(default=False)
    has_face = models.BooleanField(default=False)
    has_voice = models.BooleanField(default=False)

    voucher = models.TextField(blank=True, null=True)

    headline = models.TextField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    hobbies = models.TextField(blank=True, null=True)

    datetime_last_writing = models.DateTimeField(default=None, null=True, blank=True)
    datetime_last_face = models.DateTimeField(default=None, null=True, blank=True)
    datetime_last_voice = models.DateTimeField(default=None, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return str(self.first_name)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)


class UserExperience(ParanoidModel):
    # Choices
    USER_EXPERIENCE_TYPES = (("E", "Education"), ("W", "Work"))

    # Relationships
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

    # Fields
    type = models.TextField(
        max_length=1, choices=USER_EXPERIENCE_TYPES, default=USER_EXPERIENCE_TYPES[0]
    )
    name = models.TextField(blank=True)
    subname = models.TextField(blank=True)
    description = models.TextField(blank=True)
    date_start = models.DateField(null=True)
    date_end = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return str(self.pk)
