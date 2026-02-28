from django.db import models


class Ballot(models.Model):
    debate = models.ForeignKey('draws.Debate', on_delete=models.CASCADE, related_name='ballots')
    adjudicator = models.ForeignKey(
        'adjudication.Adjudicator', on_delete=models.SET_NULL, null=True, blank=True
    )
    confirmed = models.BooleanField(default=False)
    discarded = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Ballot {self.id} for debate {self.debate_id}'


class TeamResult(models.Model):
    POSITION_OG = 'OG'
    POSITION_OO = 'OO'
    POSITION_CG = 'CG'
    POSITION_CO = 'CO'
    POSITION_CHOICES = [
        ('OG', 'Opening Government'),
        ('OO', 'Opening Opposition'),
        ('CG', 'Closing Government'),
        ('CO', 'Closing Opposition'),
    ]

    ballot = models.ForeignKey(Ballot, on_delete=models.CASCADE, related_name='team_results')
    team = models.ForeignKey('participants.Team', on_delete=models.CASCADE)
    position = models.CharField(max_length=2, choices=POSITION_CHOICES)
    rank = models.IntegerField()  # 1=1st, 2=2nd, 3=3rd, 4=4th
    total_points = models.IntegerField(default=0)

    class Meta:
        ordering = ['rank']

    def __str__(self):
        return f'{self.team} rank {self.rank} in ballot {self.ballot_id}'


class SpeakerResult(models.Model):
    ballot = models.ForeignKey(Ballot, on_delete=models.CASCADE, related_name='speaker_results')
    speaker = models.ForeignKey('participants.Speaker', on_delete=models.CASCADE)
    score = models.FloatField()
    position_in_team = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.speaker} scored {self.score} in ballot {self.ballot_id}'
