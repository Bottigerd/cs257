#!/usr/bin/env python3
'''
    flask_sample.py
    Jeff Ondich, 22 April 2016
    Updated 7 October 2020

    A slightly more complicated Flask sample app than the
    "hello world" app found at http://flask.pocoo.org/.
'''
import sys
import argparse
import flask
import json
import psycopg2

from config import password
from config import database
from config import user
from config import port

app = flask.Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, Citizen of CS257.'

@app.route('/games')
def get_olympics():
    ''' Returns the list of olympic games, includes ID, year, season, and city. '''
    game_list = []
    query = ''' SELECT olympics.id, olympics.year, olympics.season, olympics.city 
                FROM olympics
                ORDER BY olympics.year ASC;
            '''
    try:
        cursor.execute(query)
    except Exception as e:
        print(e)
        exit()

    for row in cursor:
        game_list.append({'id':row[0], 'year':row[1], 'season':row[2], 'city':row[3]})
    return json.dumps(game_list)

@app.route('/nocs')
def get_nocs():
    ''' Returns the list of olymlpic NOCs, includes name and abbrivation. '''
    noc_list = []
    query = ''' SELECT noc_regions.noc, noc_regions.region 
                FROM noc_regions
                ORDER BY noc_regions.noc ASC;
            '''
    try:
        cursor.execute(query)
    except Exception as e:
        print(e)
        exit()

    for row in cursor:
        noc_list.append({'noc':row[0], 'region':row[1]})
    return json.dumps(noc_list)

@app.route('/medalists/games/<games_id>')
def get_medalists(games_id):
    ''' Returns the athlete's medals in each event for an olympic game.
        An NOC can be specified to only get the athletes from that NOC in that olympics game.
    '''
    
    medals_list = []

    noc = flask.request.args.get('noc', default=None)

    if noc == None:
        query = ''' SELECT olympian_athletes.id, olympian_athletes.name, olympian_athletes.sex, olympic_events.sport, olympic_events.event, olympic_event_results.medal
                FROM olympian_athletes, olympic_events, olympic_event_results
                WHERE olympian_athletes.id = olympic_event_results.olympian_id 
                AND olympic_event_results.olympic_event_id = olympic_events.id
                AND olympic_event_results.olympic_id = {0}
                AND NOT olympic_event_results.medal = 'NA'
                ORDER BY olympian_athletes.name ASC;
            '''.format(games_id)
    else:
        query = ''' SELECT DISTINCT olympian_athletes.id, olympian_athletes.name, olympian_athletes.sex, olympic_events.sport, olympic_events.event, olympic_event_results.medal
                FROM olympian_athletes, olympic_events, olympic_event_results, noc_regions, per_olympic_athlete_data
                WHERE olympian_athletes.id = olympic_event_results.olympian_id
                AND olympic_event_results.olympic_event_id = olympic_events.id
                AND olympic_event_results.olympic_id = {0}
                AND NOT olympic_event_results.medal = 'NA'
                AND olympian_athletes.id = per_olympic_athlete_data.olympian_id
                AND CAST(per_olympic_athlete_data.noc as int) = CAST(noc_regions.id as int)
                AND noc_regions.noc = UPPER('{1}')
                ORDER BY olympian_athletes.name ASC;
            '''.format(games_id, noc)

    try:
        cursor.execute(query)
    except Exception as e:
        print(e)
        exit()
    
    for row in cursor:
        medals_list.append({'id':row[0], 'name':row[1], 'sex':row[2], 'sport':row[3], 'event':row[4], 'medal':row[5]})
    return json.dumps(medals_list)
    
@app.route('/movies')
def get_movies():
    ''' Returns the list of movies that match GET parameters:
          start_year, int: reject any movie released earlier than this year
          end_year, int: reject any movie released later than this year
          genre: reject any movie whose genre does not match this genre exactly
        If a GET parameter is absent, then any movie is treated as though
        it meets the corresponding constraint. (That is, accept a movie unless
        it is explicitly rejected by a GET parameter.)
    '''
    movie_list = []
    genre = flask.request.args.get('genre')
    start_year = flask.request.args.get('start_year', default=0, type=int)
    end_year = flask.request.args.get('end_year', default=10000, type=int)
    for movie in movies:
        if genre is not None and genre != movie['genre']:
            continue
        if movie['year'] < start_year:
            continue
        if movie['year'] > end_year:
            continue
        movie_list.append(movie)

    return json.dumps(movie_list)

if __name__ == '__main__':
    try:
        connection = psycopg2.connect(database=database, user=user, password=password, port=port)
    except Exception as e:
        print(e)
        exit()

    cursor = connection.cursor()

    parser = argparse.ArgumentParser('A olympic database Flask application/API')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)
