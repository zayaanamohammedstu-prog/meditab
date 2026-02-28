from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=100)
    tournament = models.ForeignKey('tournaments.Tournament', on_delete=models.CASCADE, related_name='rooms')
    priority = models.IntegerField(default=0)

    class Meta:
        ordering = ['-priority', 'name']

    def __str__(self):
        return self.name


class Round(models.Model):
    DRAW_TYPE_RANDOM = 'random'
    DRAW_TYPE_POWER = 'power'
    DRAW_TYPE_ELIM = 'elim'
    DRAW_TYPE_CHOICES = [
        ('random', 'Random'),
        ('power', 'Power Paired'),
        ('elim', 'Elimination'),
    ]

    STATUS_DRAFT = 'draft'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_RELEASED = 'released'
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('released', 'Released'),
    ]

    tournament = models.ForeignKey(
        'tournaments.Tournament', on_delete=models.CASCADE, related_name='rounds'
    )
    seq = models.IntegerField()
    name = models.CharField(max_length=100)
    draw_type = models.CharField(max_length=20, choices=DRAW_TYPE_CHOICES, default=DRAW_TYPE_RANDOM)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    motion = models.TextField(blank=True)
    info_slide = models.TextField(blank=True)
    is_break_round = models.BooleanField(default=False)
    starts_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['seq']
        unique_together = [('tournament', 'seq')]

    def __str__(self):
        return f'{self.tournament} - {self.name}'


class Debate(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE, related_name='debates')
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    og_team = models.ForeignKey(
        'participants.Team', on_delete=models.SET_NULL, null=True, blank=True, related_name='og_debates'
    )
    oo_team = models.ForeignKey(
        'participants.Team', on_delete=models.SET_NULL, null=True, blank=True, related_name='oo_debates'
    )
    cg_team = models.ForeignKey(
        'participants.Team', on_delete=models.SET_NULL, null=True, blank=True, related_name='cg_debates'
    )
    co_team = models.ForeignKey(
        'participants.Team', on_delete=models.SET_NULL, null=True, blank=True, related_name='co_debates'
    )

    def __str__(self):
        return f'{self.round} - {self.room}'

    def get_chair(self):
        da = self.debate_adjudicators.filter(adj_type=DebateAdjudicator.TYPE_CHAIR).first()
        return da.adjudicator if da else None

    def get_panelists(self):
        return [
            da.adjudicator
            for da in self.debate_adjudicators.filter(adj_type=DebateAdjudicator.TYPE_PANELIST)
        ]


class DebateAdjudicator(models.Model):
    TYPE_CHAIR = 'chair'
    TYPE_PANELIST = 'panelist'
    TYPE_TRAINEE = 'trainee'
    TYPE_CHOICES = [
        ('chair', 'Chair'),
        ('panelist', 'Panelist'),
        ('trainee', 'Trainee'),
    ]
    debate = models.ForeignKey(Debate, on_delete=models.CASCADE, related_name='debate_adjudicators')
    adjudicator = models.ForeignKey('adjudication.Adjudicator', on_delete=models.CASCADE)
    adj_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=TYPE_PANELIST)

    def __str__(self):
        return f'{self.adjudicator} ({self.adj_type}) in {self.debate}'
