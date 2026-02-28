from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_ADMIN = 'admin'
    ROLE_TAB_DIRECTOR = 'tab_director'
    ROLE_ADJUDICATOR = 'adjudicator'
    ROLE_PARTICIPANT = 'participant'
    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_TAB_DIRECTOR, 'Tab Director'),
        (ROLE_ADJUDICATOR, 'Adjudicator'),
        (ROLE_PARTICIPANT, 'Participant'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_PARTICIPANT)

    def __str__(self):
        return self.username

    def is_tab_director(self):
        return self.role in (self.ROLE_ADMIN, self.ROLE_TAB_DIRECTOR) or self.is_staff
