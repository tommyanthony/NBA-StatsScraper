from sqlalchemy import (Column, ForeignKey, Integer, DECIMAL, String, BOOLEAN,
                        create_engine)
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class Player(Base):
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(250), nullable=False)
    last_name = Column(String(250), nullable=False)
    full_name = Column(String(250), nullable=False)  # Last, First
    active = Column(BOOLEAN)
    from_year = Column(Integer)
    to_year = Column(Integer)


class Team(Base):
    __tablename__ = 'team'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    from_year = Column(Integer)
    to_year = Column(Integer)
    active = Column(BOOLEAN)
    conference = Column(String(250))
    division = Column(String(100))
    abbreviation = Column(String(3))


class StatLine():
    @declared_attr
    def player_id(cls):
        return Column(Integer, ForeignKey('player.id'))

    year = Column(Integer)
    season = Column(String(25))

    games_played = Column(Integer)
    minutes = Column(DECIMAL(8, 4))
    fouls = Column(DECIMAL(8, 4))

    fgm = Column(DECIMAL(8, 4))
    fga = Column(DECIMAL(8, 4))
    fg_pct = Column(DECIMAL(8, 4))

    ftm = Column(DECIMAL(8, 4))
    fta = Column(DECIMAL(8, 4))
    ft_pct = Column(DECIMAL(8, 4))

    fg3m = Column(DECIMAL(8, 4))
    fg3a = Column(DECIMAL(8, 4))
    fg3_pct = Column(DECIMAL(8, 4))

    @property
    def effective_fg(self):
        real_fgm = float(self.fgm) + .5 * float(self.fg3m)
        return 100 * real_fgm / float(self.fga)

    offensive_rebounds = Column(DECIMAL(8, 4))
    defensive_rebounds = Column(DECIMAL(8, 4))
    rebounds = Column(DECIMAL(8, 4))

    assists = Column(DECIMAL(8, 4))
    steals = Column(DECIMAL(8, 4))
    blocks = Column(DECIMAL(8, 4))
    turnovers = Column(DECIMAL(8, 4))
    points = Column(DECIMAL(8, 4))


class TotalLines(StatLine, Base):
    """
    Inherits from StatLine
    """
    __tablename__ = 'season'
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('team.id'))
    age = Column(Integer)
    games_started = Column(Integer)


class SplitLines(StatLine, Base):
    """
    Inherits from StatLine
    """
    __tablename__ = 'splitline'
    id = Column(Integer, primary_key=True)
    tag = Column(String(250), nullable=False)
    wins = Column(Integer)
    losses = Column(Integer)
    win_pct = Column(DECIMAL(5, 4))
    plus_minus = Column(DECIMAL(8, 4))


class Split(Base):
    __tablename__ = 'split'
    id = Column(Integer, primary_key=True)
    type = Column(String(250), nullable=False)
    first = Column(Integer, ForeignKey('splitline.id'))
    second = Column(Integer, ForeignKey('splitline.id'))

NAME = 'test'
DRIVER = 'pymysql'
HOST = 'localhost'
URL = 'mysql+%s://root@%s/%s' % (DRIVER, HOST, NAME)


def create_db_session():
    engine = create_engine(URL)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()


def create_tables():
    Base.metadata.create_all(create_engine(URL))
