from django.db import models


class Adjudicator(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    institution = models.ForeignKey(
        'participants.Institution', on_delete=models.SET_NULL, null=True, blank=True
    )
    tournament = models.ForeignKey(
        'tournaments.Tournament', on_delete=models.CASCADE, related_name='adjudicators'
    )
    base_score = models.FloatField(default=75.0)
    independent = models.BooleanField(default=False)
    user = models.OneToOneField(
        'accounts.User', on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        ordering = ['-base_score', 'name']

    def __str__(self):
        return self.name

    def current_score(self):
        feedback = self.feedback_received.filter()
        if not feedback.exists():
            return self.base_score
        scores = [f.score for f in feedback]
        return round(sum(scores) / len(scores), 2)


class AdjudicatorConflict(models.Model):
    CONFLICT_PERSONAL = 'personal'
    CONFLICT_INSTITUTION = 'institution'
    CONFLICT_CHOICES = [
        (CONFLICT_PERSONAL, 'Personal'),
        (CONFLICT_INSTITUTION, 'Institutional'),
    ]
    adjudicator = models.ForeignKey(Adjudicator, on_delete=models.CASCADE, related_name='conflicts')
    team = models.ForeignKey(
        'participants.Team', on_delete=models.CASCADE, null=True, blank=True
    )
    conflict_type = models.CharField(
        max_length=20, choices=CONFLICT_CHOICES, default=CONFLICT_PERSONAL
    )

    def __str__(self):
        return f'{self.adjudicator} conflicts with {self.team}'


class AdjudicatorFeedback(models.Model):
    adjudicator = models.ForeignKey(
        Adjudicator, on_delete=models.CASCADE, related_name='feedback_received'
    )
    debate = models.ForeignKey('draws.Debate', on_delete=models.CASCADE)
    source_adjudicator = models.ForeignKey(
        Adjudicator, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='feedback_given'
    )
    score = models.FloatField()
    comments = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Feedback for {self.adjudicator} in debate {self.debate_id}'
