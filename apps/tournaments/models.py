from django.db import models
from django.urls import reverse


class Tournament(models.Model):
    FORMAT_BP = 'BP'
    FORMAT_WSDC = 'WSDC'
    FORMAT_CHOICES = [
        (FORMAT_BP, 'British Parliamentary'),
        (FORMAT_WSDC, 'WSDC'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    institution = models.CharField(max_length=200, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default=FORMAT_BP)
    num_prelim_rounds = models.IntegerField(default=5)
    num_break_rounds = models.IntegerField(default=2)
    break_size = models.IntegerField(default=8)
    motions_public = models.BooleanField(default=False)
    tab_released = models.BooleanField(default=False)
    registration_open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tournaments:detail', kwargs={'slug': self.slug})
