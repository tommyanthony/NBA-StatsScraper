from abstract import Endpoint, new_api
import parameters as params

api = new_api("http://stats.nba.com/stats/")

"""
This file defines the parts of stats.nba.com's API that is accessible. To
access the API import the api object from this file
"""

@api.endpoint()
class PlayerID(Endpoint):
    __optional_params__ = {
        "isOnlyCurrentSeason": params.TRUE,
        "LeagueID": params.LeagueID.NBA
    }
    __required_params__ = ['Season']
    __endpoint__ = "commonallplayers"


@api.endpoint()
class PlayerGameLogEndpoint(Endpoint):
    # http://stats.nba.com/stats/playergamelog?LeagueID=00&PlayerID=201939&Season=2014-15&SeasonType=Playoffs
    __optional_params__ = {
        "SeasonType": params.SeasonType.REGULAR_SEASON,
    }
    __required_params__ = ['Season', 'PlayerID']
    __endpoint__ = "playergamelog"


@api.endpoint()
class PlayerSplits(Endpoint):
    __optional_params__ = {
        "SeasonType": params.SeasonType.REGULAR_SEASON,
        "LeagueID": params.LeagueID.NBA,
        "PerMode": params.PerMode.PER_GAME,
        "DateFrom": "", "DateTo": "", "GameSegment": "", "LastNGames": "0",
        "Location": "", "MeasureType": "Base", "Month": "0",
        "OpponentTeamID": "0", "Outcome": "", "PaceAdjust": params.NO,
        "PlusMinus": params.NO, "Rank": params.NO, "Period": 0,
        "VsConference": "", "VsDivision": "", "SeasonSegment": ""
    }
    __required_params__ = ['Season', 'PlayerID']
    __endpoint__ = "playerdashboardbygeneralsplits"


@api.endpoint()
class PlayerCareerStats(Endpoint):
    __optional_params__ = {
        "LeagueID": params.LeagueID.NBA,
        "PerMode": params.PerMode.PER_GAME,
    }
    __required_params__ = ['PlayerID']
    __endpoint__ = "playercareerstats"
