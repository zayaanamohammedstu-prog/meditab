from django.db import models


class Institution(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=10)
    region = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.code} - {self.name}'


class Team(models.Model):
    name = models.CharField(max_length=200)
    code_name = models.CharField(max_length=50, blank=True)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, null=True, blank=True)
    tournament = models.ForeignKey('tournaments.Tournament', on_delete=models.CASCADE, related_name='teams')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def total_points(self):
        from apps.results.models import TeamResult
        result = TeamResult.objects.filter(
            team=self, ballot__confirmed=True
        ).aggregate(total=models.Sum('total_points'))
        return result['total'] or 0

    def wins(self):
        from apps.results.models import TeamResult
        return TeamResult.objects.filter(team=self, rank=1, ballot__confirmed=True).count()


class Speaker(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='speakers')
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.OneToOneField('accounts.User', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def average_score(self):
        from apps.results.models import SpeakerResult
        results = SpeakerResult.objects.filter(speaker=self, ballot__confirmed=True)
        if not results.exists():
            return 0
        total = sum(r.score for r in results)
        return round(total / results.count(), 2)
