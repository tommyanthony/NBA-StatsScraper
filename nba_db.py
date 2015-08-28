import schema
from schema import (Team, Player, TotalLines)
from functools import reduce
import operator

class Filter(object):
    def __init__(self):
        self.filters = []

    def add(self, f):
        self.filters.append(f)

    def get(self):
        return reduce(operator.and_, self.filters)

class NBADB(object):
    def __init__(self):
        self.session = schema.create_db_session()

    def commit(self):
        self.session.commit()

    def get_team_from_abbrev(self, abbrev, year):
        return self.team(abbrev=abbrev, year=year)

    def team(self, team_id=None, abbrev=None, year=None):
        f = Filter()
        if year:
            f.add((Team.from_year <= year) & (Team.to_year >= year))
        if team_id:
            f.add(Team.id == team_id)
        if abbrev:
            f.add(Team.abbreviation == abbrev)
        return self.session.query(Team).filter(f.get()).one()

    def add_player(self, player_kwargs):
        player = Player(**player_kwargs)
        self.session.add(player)
        return player

    def add_season(self, stats, player_id):
        season = schema.TotalLines(player_id=player_id, **stats)
        self.session.add(season)
        return season
