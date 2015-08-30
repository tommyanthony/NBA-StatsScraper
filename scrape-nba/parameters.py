# This class contains the parameters for the backend API.
TRUE = 1
FALSE = 0

YES = 'Y'
NO = 'N'

LAST_SEASON = '2013-14'
CURRENT_SEASON = '2014-15'

class LeagueID():
    NBA = '00'
    WNBA = '10'
    D_LEAGUE = '20'

class SeasonType():
    REGULAR_SEASON = 'Regular Season'
    POST_SEASON = 'Playoffs'
    ALL_STAR_SEASON = 'All Star'

class PerMode():
    TOTALS = 'Totals'
    PER_GAME = 'PerGame'
    MINUTES_PER = 'MinutesPer'
    PER_48 = 'Per48'
    PER_40 = 'Per40'
    PER_36 = 'Per36'
    PER_MINUTE = 'PerMinute'
    POSSESSION = 'PerPossession'
    PLAY = 'PerPlay'
    PER_100_POSSESSIONS = 'Per100Possessions'
    PER_100_PLAYS = 'Per100Plays'
