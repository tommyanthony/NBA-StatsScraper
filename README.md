# NBA Stats Downloader
This tool downloads data from stats.nba.com and stores it in a SQL database.  The default is MySQL, but can be changed in schema.py as the code us SQLAlchemy so any SQL database supported by SQLAlchemy should be able to be used.   

## About
stats.nba.com uses AngularJS for it's websites, and the backend exposes JSON ednpoints that the data is loaded from.  This takes the JSON data and dumps it into a SQL database.

## What's supported?
Currently all the data it draws is about players full-length per-game season stats and their pre-post trade stats splits. Support for season totals is planned.  If you want some other data, request it and I'll add it.

## How to use
The requirements can be installed via pip:
```shell
pip install -r requirements.txt
```

The database is set up by first executing schema.py, and then the data is imported using json_to_db.py

schema.py defaults to MySQL running on the localmachine with a database name of test.

To set up the tables, one can simply run
```shell
python schema.py
```
which will call the create_tables function defined in schema.py.

To see all options
```shell
python schema.py --help
Usage: schema.py [OPTIONS]

  Options change the fields used by SQLAlchemy to connect to the database

Options:
  --db_name TEXT   Database name
  --sql_type TEXT  SQL Type (ex. MySQL)
  --driver TEXT    Driver used to connect
  --host TEXT      DB host
  --user TEXT      DB user
  --password TEXT  DB password
  --help           Show this message and exit.
```


To import the data, run
```shell
python json_to_db.py
```
By default, this will currently only import all active players, all players can be done and different season can be changed using the command line flags:
```shell
python json_to_db.py --help
Usage: json_to_db.py [OPTIONS]

  Example usage:

  python json_to_db.py --season 2013-14

  python json_to_db.py --all

Options:
  --season TEXT  Season of data to downloadexample values: '2014-15',
                 '2012-13'
  --current      Only import the currently active players
  --all          Import all players from NBA history
  --help         Show this message and exit.
 ```

