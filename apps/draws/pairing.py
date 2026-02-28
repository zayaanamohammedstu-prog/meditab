"""
BP Power Pairing Algorithm

For prelim rounds:
- Round 1: Random pairing
- Subsequent rounds: Power-pair based on wins then total speaker points

BP positions assigned to balance position history where possible.
"""
import random
from collections import defaultdict
from apps.participants.models import Team
from apps.results.models import TeamResult
from .models import Debate, Room


def get_team_stats(tournament):
    """Return dict of team_id -> {wins, points, position_counts}."""
    stats = {}
    teams = Team.objects.filter(tournament=tournament)
    for team in teams:
        results = TeamResult.objects.filter(team=team, ballot__confirmed=True)
        wins = results.filter(rank=1).count()
        points = sum(r.total_points for r in results)
        pos_counts = defaultdict(int)
        for r in results:
            pos_counts[r.position] += 1
        stats[team.id] = {
            'team': team,
            'wins': wins,
            'points': points,
            'position_counts': pos_counts,
        }
    return stats


def assign_positions(debates, stats):
    """
    Assign OG/OO/CG/CO positions to teams in each debate,
    trying to balance position history.
    """
    position_order = ['OG', 'OO', 'CG', 'CO']
    for debate in debates:
        teams = list(debate['teams'])
        # Sort teams by position balance (least-used positions first)
        def position_score(team):
            s = stats.get(team.id, {}).get('position_counts', {})
            # prefer positions used least
            return tuple(s.get(p, 0) for p in position_order)

        teams.sort(key=position_score)
        debate['og'] = teams[0]
        debate['oo'] = teams[1]
        debate['cg'] = teams[2]
        debate['co'] = teams[3]
    return debates


def generate_random_draw(tournament, round_obj):
    """Generate a random draw for round 1."""
    teams = list(Team.objects.filter(tournament=tournament))
    random.shuffle(teams)

    # Groups of 4 for BP
    debates_data = []
    for i in range(0, len(teams) - 3, 4):
        debates_data.append({'teams': teams[i:i+4]})

    stats = get_team_stats(tournament)
    debates_data = assign_positions(debates_data, stats)
    return _create_debates(round_obj, debates_data, tournament)


def generate_power_paired_draw(tournament, round_obj):
    """Generate a power-paired draw based on wins then points."""
    teams = list(Team.objects.filter(tournament=tournament))
    stats = get_team_stats(tournament)

    # Sort by wins desc, then points desc, then random for tiebreaking
    teams.sort(key=lambda t: (
        -stats.get(t.id, {}).get('wins', 0),
        -stats.get(t.id, {}).get('points', 0),
        random.random()
    ))

    debates_data = []
    for i in range(0, len(teams) - 3, 4):
        debates_data.append({'teams': teams[i:i+4]})

    debates_data = assign_positions(debates_data, stats)
    return _create_debates(round_obj, debates_data, tournament)


def _create_debates(round_obj, debates_data, tournament):
    """Create Debate objects from pairing data."""
    rooms = list(Room.objects.filter(tournament=tournament).order_by('-priority'))
    created = []
    for idx, d in enumerate(debates_data):
        room = rooms[idx] if idx < len(rooms) else None
        debate = Debate.objects.create(
            round=round_obj,
            room=room,
            og_team=d.get('og'),
            oo_team=d.get('oo'),
            cg_team=d.get('cg'),
            co_team=d.get('co'),
        )
        created.append(debate)
    return created


def generate_draw(tournament, round_obj):
    """Main entry point: generate draw based on round draw_type."""
    # Delete existing debates for this round
    round_obj.debates.all().delete()

    if round_obj.draw_type == 'random' or round_obj.seq == 1:
        return generate_random_draw(tournament, round_obj)
    elif round_obj.draw_type == 'power':
        return generate_power_paired_draw(tournament, round_obj)
    else:
        # Elimination rounds - power paired
        return generate_power_paired_draw(tournament, round_obj)
