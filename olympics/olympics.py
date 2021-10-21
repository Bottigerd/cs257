#!/usr/bin/env python3
'''
    olympics.py
    Dani Bottiger

    Based off Jeff Ondich's psycopg2-sample.py from:
    https://github.com/ondich/cs257_2021_fall.git

    olympics.py is a CLI to obtain information on the olympic PSQL database.

'''
import psycopg2
import argparse

from config import password
from config import database
from config import user
from config import port

class database_searches:
    def print_help(self):
        '''
        Prints the usage.txt for usage instructions.
        '''
        f = open('usage.txt', 'r')
        content = f.read()
        print(content)
        f.close()

    def list_NOC_athletes(self, noc=''):
        '''
        List the names of all the athletes from a specified NOC.
        We can search by NOC id or NOC name.
        '''
        if noc.isnumeric():
            query = '''SELECT DISTINCT olympian_athletes.id, olympian_athletes.name 
                    FROM olympian_athletes, per_olympic_athlete_data, noc_regions
                    WHERE CAST(per_olympic_athlete_data.noc as int) = %s
                    AND per_olympic_athlete_data.olympian_id = olympian_athletes.id;'''
        else:
            query = '''SELECT DISTINCT olympian_athletes.id, olympian_athletes.name 
                    FROM olympian_athletes, per_olympic_athlete_data, noc_regions
                    WHERE CAST(per_olympic_athlete_data.noc as int) = CAST(noc_regions.id as int)
                    AND noc_regions.noc = UPPER(%s)
                    AND per_olympic_athlete_data.olympian_id = olympian_athletes.id;'''
        try:
            cursor.execute(query, (noc,))
        except Exception as e:
            print(e)
            print()
            self.print_help()
            exit()

        # No use printing out the headers if we don't have any results. So, let's check.
        if cursor.rowcount == 0:
            if noc.isnumeric():
                print("Search of Athletes in NOC ID {0} yielded 0 results.".format(noc))
            else:
                print("Search of Athletes in {0} yielded 0 results.".format(noc))
            print('''Type "python3 olympics.py -h" to see the usage documentation''')
        else:
            if noc.isnumeric():
                print('===== Athletes in NOC ID {0} ====='.format(noc))
            else:
                print('===== Athletes in {0} ====='.format(noc))
            print('ATHLETE ID | ATHLETE NAME')
            print('=========================')
            for row in cursor:
                print(str(row[0]) + " | " + str(row[1]))
            print()

    def list_NOC_medals_rankings(self):
        '''
        List all the NOCs and the number of gold medals they have won
        Listed in decreasing order of the number of gold medals.
        '''
        query = '''SELECT noc_regions.noc, noc_regions.region, COUNT(olympic_event_results.medal) 
                FROM olympic_event_results, noc_regions, per_olympic_athlete_data 
                WHERE olympic_event_results.medal = 'Gold'
                AND olympic_event_results.olympian_id = per_olympic_athlete_data.olympian_id
                AND CAST(per_olympic_athlete_data.noc AS integer) = noc_regions.id
                GROUP BY noc_regions.noc, noc_regions.region
                ORDER BY COUNT(olympic_event_results.medal) DESC;'''
        try:
            cursor.execute(query)
        except Exception as e:
            print(e)
            print()
            self.print_help()
            exit()

        print('===== NOC Number of Gold Medals Ranked =====')
        print('NOC | REGION/COUNTRY | # OF GOLD MEDALS')
        print('=======================')
        for row in cursor:
            print(str(row[0]) + " | " + str(row[1]) + " | " + str(row[2]))
        print()

    def list_athletes_medals(self, athlete=''):
        '''
        List of the athletes yeilded by the search term, athlete, and their medals
        Listed alphabetically by year, athlete and then event.
        '''
        if athlete.isnumeric():
            query = '''SELECT olympics.year, olympian_athletes.name, olympic_events.event, olympic_event_results.medal 
                    FROM olympic_event_results, olympics, olympic_events, olympian_athletes
                    WHERE olympic_event_results.olympian_id = {0}
                    AND NOT olympic_event_results.medal = 'NA' 
                    AND olympian_athletes.id = {0}
                    AND olympic_event_results.olympic_id = olympics.id 
                    AND olympic_event_results.olympic_event_id = olympic_events.id 
                    ORDER BY olympics.year, olympian_athletes.name, olympic_events.event ASC;'''.format(athlete)
        else:
            query = '''SELECT olympics.year, olympian_athletes.name, olympic_events.event, olympic_event_results.medal 
                    FROM olympic_event_results, olympics, olympic_events, olympian_athletes 
                    WHERE olympic_event_results.olympian_id = olympian_athletes.id
                    AND UPPER(olympian_athletes.name) LIKE UPPER('%%{0}%%')
                    AND NOT olympic_event_results.medal = 'NA' 
                    AND olympic_event_results.olympic_id = olympics.id 
                    AND olympic_event_results.olympic_event_id = olympic_events.id  
                    ORDER BY olympics.year, olympian_athletes.name, olympic_events.event ASC; '''.format(athlete)
        try:
            cursor.execute(query, (athlete,))
        except Exception as e:
            print(e)
            print()
            self.print_help()
            exit()
        
        # No use printing out the headers if we don't have any results. So, let's check.
        if cursor.rowcount == 0:
            if athlete.isnumeric():
                print("Search of Athlete ID {0}'s medals yielded 0 results.".format(athlete))
            else:
                print("Search of {0}'s medals yielded 0 results.".format(athlete))
            print('''Type "python3 olympics.py -h" to see the usage documentation''')
        else:
            if athlete.isnumeric:
                print("===== Medals of ID {0} =====".format(athlete))
            else:
                print("===== {0}'s Medals =====".format(athlete))
            print(' Year | Athlete | Event | Medal')
            print('===============================')
            for row in cursor:
                print(str(row[0]) + " | " + str(row[1]) + " | " + str(row[2]) + " | " + str(row[3]))
            print()

# Connect to the database
try:
    connection = psycopg2.connect(database=database, user=user, password=password, port=port)
except Exception as e:
    print(e)
    exit()

# Argparse
parser = argparse.ArgumentParser(add_help=False)

parser.add_argument('-h', '--help', action='store_true', help='show usage.txt')
parser.add_argument('-a', '--athletes_medals', action='store_true', help="show athlete's medals")
parser.add_argument('-n', '--noc', action='store_true', help="show noc's members")
parser.add_argument('-m', '--medal_rankings', action='store_true', help="rank NOCs by gold medal count")

parser.add_argument('search_term', metavar='search_term', nargs='?', help="search input for search tags")

args = parser.parse_args()

# Using the database
cursor = connection.cursor()
database_searches = database_searches()

if args.help:
    database_searches.print_help()
elif args.noc:
    if args.search_term == None:
        print("An NOC is required to search for its athletes.")
        print()
        database_searches.print_help()
    else:
        database_searches.list_NOC_athletes(args.search_term)
elif args.medal_rankings:
    database_searches.list_NOC_medals_rankings()
else:
    if args.search_term == None:
        print("A search term is required for an athlete's medals search.")
        print()
        database_searches.print_help()
    else:
        database_searches.list_athletes_medals(args.search_term)

# Closing the database connection.
connection.close()

