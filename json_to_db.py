import parameters
from convert_maps import STATS_MAP
from import_teams import import_teams
from nba_stats import api
from nba_db import NBADB
from collections import defaultdict



def create(season, currentSeason=parameters.TRUE):
    import_teams()
    db = NBADB()
    load_all_players(season, db, currentSeason)


def load_all_players(season, db, currentSeason):
    json = api.commonallplayers(Season=season,
                                isOnlyCurrentSeason=currentSeason)
    for player in json.data[0]['rowSet']:
        nba_id = player[0]
        player_kwargs = extract_player(player)
        player_obj = db.add_player(player_kwargs)
        career_averages, pre_post_trade = load_career_averages(nba_id, db)
        for season in career_averages:
            db.add_season(season, player_obj.id)
        # TODO change add_season, add in pre_post_trade
        if pre_post_trade:
            num_trades = len(pre_post_trade) - 1
            for trade in range(num_trades):
                pass
    db.commit()


def extract_player(json_player):
    names = json_player[1].split(', ')
    if len(names) != 2:
        if json_player[1] == 'Nene':
            # for some reason stats.nba.com doesn't have Nene's last name
            json_player[1] = 'Hilario, Nene'
            names = ('Hilario', 'Nene')
        else:
            raise Exception(json_player[1])
    return {
        'full_name': json_player[1],
        'first_name': names[1],
        'last_name': names[0],
        'active': bool(json_player[2]),
        'from_year': int(json_player[3]),
        'to_year': int(json_player[4])
    }


def load_career_averages(nba_id, db):
    json = api.playercareerstats(PlayerID=nba_id)
    return extract_career_averages(json.data, db)

def extract_career_averages(json_averages, db):
    all_averages = []
    for season_type in json_averages:
        if season_type['name'] == 'SeasonTotalsRegularSeason':
            for season in season_type['rowSet']:
                data = dict(zip(season_type['headers'], season))
                avgs = {STATS_MAP[key]: value for key, value in data.items()
                        if key in STATS_MAP}
                year = int(avgs['season'][:4])
                team = db.get_team_from_abbrev(data['TEAM_ABBREVIATION'], year)
                avgs['team_id'] = team.id
                avgs['year'] = year
                all_averages.append(avgs)
    years = [season['year'] for season in all_averages]
    total_team = db.team(abbrev='TOT')
    career_averages = []
    pre_post_trade = defaultdict(list)
    for season in all_averages:
        year = season['year']
        if years.count(year) > 1:
            if season['team_id'] == total_team.id:
                career_averages.append(season)
            else:
                pre_post_trade[year].append(season)
        else:
            career_averages.append(season)
    return career_averages, pre_post_trade


"""
The code below handles the command line interface for importing the data
"""
import click

@click.command()
@click.option('--season', default=parameters.CURRENT_SEASON,
              help='Season of data to download, ex. 2014-15, 2012-13')
@click.option('--current', 'current_season', flag_value=parameters.TRUE,
              default=True, help='Only import the currently active players')
@click.option('--all', 'current_season', flag_value=parameters.FALSE,
              help='Import all players from NBA history')
def cli(season, current_season):
    create(season, current_season)

if __name__ == "__main__":
    cli()
