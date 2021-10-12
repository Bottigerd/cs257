'''
Dani Bottiger
CS 257 SOFTWARE DESIGN - Fall 2021
Database Design Assignment

convert.py reads a large csv file on olympic events and their results and creates multiple csv files based
on the orignal. These smaller csv files are then put into an olympic database.
'''
import csv

class olympic_db:
    def __init__(self, athlete_events_raw='', noc_regions_raw=''):
        '''
        Reads our athlete_event csv file from
            kaggle.com/heesoo37/120-years-of-olympic-history-athletes-and-results
        to convert it into more bit-size csv files for a database.

        Columns in athlete_events_raw:
            0   1     2    3    4       5       6     7    8      9     10      11    12     13     14     
            ID, Name, Sex, Age, Height, Weight, Team, NOC, Games, Year, Season, City, Sport, Event, Medal
        
        Columns in noc_regions:
            0    1       2
            NOC, region, notes
        '''
        self.athlete_events_raw = self.read_csv_file(athlete_events_raw)
        self.noc_regions = self.read_csv_file(noc_regions_raw)
        print("Raw data aquired!")

        print("Beginning to sort Olympians...")
        self.olympian_athletes = self.write_athletes_csv(self.athlete_events_raw)
        print("Olympians sorted!")

        print("Beginning to sort Olympics...")
        self.olympics = self.write_olympics_csv(self.athlete_events_raw)
        print("Olympics sorted!")

        print("Beginning to sort Olympic Events...")
        self.olympic_events = self.write_olympic_events_csv(self.athlete_events_raw)
        print("Olympic Events sorted!")

        print("Beginning to sort Olympic Event Results...")
        self.olympic_event_results = self.write_olympic_event_results_csv(self.athlete_events_raw)
        print("Olympic Event Results sorted!")

        print("Beginning to sort Olympian Data...")
        self.per_olympic_athlete_data = self.write_per_olympic_athlete_data_csv(self.athlete_events_raw)
        print("Olympian Data sorted!")

        print("Done!")

    def read_csv_file(self, csv_file=''):
        file = open(csv_file)
        csvreader = csv.reader(file)
        raw_dictionary = []
        for row in csvreader:
            raw_dictionary.append(row)
        file.close()
        raw_dictionary.pop(0)
        return raw_dictionary
    
    def write_athletes_csv(self, raw_dictionary):
        '''
        From athlete_events_raw, create an olympian_athletes_list and write to a csv file.

        Columns in olympian_athletes_list:
            0   1     2    3    
            ID, Name, Sex, NOC_ID
        '''
        olympian_athletes_list = []
        for row in raw_dictionary:
            temp_athlete = []
            exists_boolean = False

            for athlete in olympian_athletes_list: # Before we do anything, let's make sure we're not adding a duplicate.
                if row[0] == athlete[0]:
                    exists_boolean = True
            if exists_boolean is False:
                temp_athlete.append(row[0]) # ID
                temp_athlete.append(row[1]) # Name
                temp_athlete.append(row[2]) # Sex

                '''
                We don't add Age, Height, or Weight since those change for those in multiple olympics.
                This will be stored with in our per_olympic_athelete table.
                '''

                noc_id_num = 1
                for noc in self.noc_regions:
                    if noc[0] == row[7]:    # Team and NOC (combined -> Team exists in NOC db)
                        temp_athlete.append(noc_id_num) # NOC_ID
                    else:
                        noc_id_num = noc_id_num + 1
                olympian_athletes_list.append(temp_athlete)

        with open('olympian_athlete_data.csv', 'w') as olympian_athlete_data_file:
            writer = csv.writer(olympian_athlete_data_file)
            writer.writerows(olympian_athletes_list)

        return olympian_athletes_list

    def write_olympics_csv(self, raw_dictionary):
        '''
        From athlete_events_raw, create an olympics_list and write to a csv file.

        Columns in olympics_list:
            0   1      2     3       4
            ID, Games, Year, Season, City
        '''
        olympics_list = []
        for row in raw_dictionary:
            temp_olympics = []
            exists_boolean = False

            for olympics in olympics_list: # Before we do anything, let's make sure we're not adding a duplicate.
                if row[8] == olympics[1]:
                    exists_boolean = True
            if exists_boolean is False:
                temp_olympics.append(len(olympics_list) + 1) # ID
                temp_olympics.append(row[8]) # Games
                temp_olympics.append(row[9]) # Year
                temp_olympics.append(row[10]) # Season
                temp_olympics.append(row[11]) # City
                olympics_list.append(temp_olympics)
        
        with open('olympics_data.csv', 'w') as olympics_data_file:
            writer = csv.writer(olympics_data_file)
            writer.writerows(olympics_list)

        return olympics_list

    def write_olympic_events_csv(self, raw_dictionary):
        '''
        From athlete_events_raw, create an olympic_events_list and write to a csv file.

        Columns in olympic_events_list:
            0   1       2      3
            ID, Season, Sport, Event
        '''
        olympic_events_list = []
        for row in raw_dictionary:
            temp_olympic_event = []
            exists_boolean = False
            
            for olympic_event in olympic_events_list:
                if row[13] == olympic_event[3]:
                    exists_boolean = True
            if exists_boolean is False:
                temp_olympic_event.append(len(olympic_events_list) + 1) # ID
                temp_olympic_event.append(row[10]) # Season
                temp_olympic_event.append(row[12]) # Sport
                temp_olympic_event.append(row[13]) # Event
                olympic_events_list.append(temp_olympic_event)

        with open('olympic_event_data.csv', 'w') as olympic_events_data_file:
            writer = csv.writer(olympic_events_data_file)
            writer.writerows(olympic_events_list)

        return olympic_events_list

    def write_olympic_event_results_csv(self, raw_dictionary):
        '''
        From athlete_events_raw, create an olympic_event_results_list and write to a csv file.

        Columns in olympic_event_results_list:
            0   1           2                 3            4
            ID, Olympic ID, Olympic Event ID, Olympian ID, Medal
        '''
        olympic_event_results_list = []
        for row in raw_dictionary:
            temp_olympic_event_result = []
            
            # This we need every value, so we won't have to check for duplicates. We do however have to find the right IDs.
            temp_olympic_event_result.append(len(olympic_event_results_list) + 1) # ID
            
            olympic_id_num = 1
            for olympics in self.olympics:
                    if olympics[1] == row[8]: # Searching for Olympic ID
                        temp_olympic_event_result.append(olympic_id_num) # Olympic ID
                    else:
                        olympic_id_num = olympic_id_num + 1
            
            olympic_event_id_num = 1
            for olympic_event in self.olympic_events:
                    if olympic_event[3] == row[13]: # Searching for Olympic Event ID
                        temp_olympic_event_result.append(olympic_event_id_num) # Olympic Event ID
                    else:
                        olympic_event_id_num = olympic_event_id_num + 1
            
            olympian_id_num = 1
            for olympian in self.olympian_athletes:
                    if olympian[0] == row[0]: # Searching for Olympian ID
                        temp_olympic_event_result.append(olympian_id_num) # Olympian ID
                    else:
                        olympian_id_num = olympian_id_num + 1

            temp_olympic_event_result.append(row[14])
            olympic_event_results_list.append(temp_olympic_event_result)

        with open('olympic_event_results_data.csv', 'w') as olympic_event_results_data_file:
            writer = csv.writer(olympic_event_results_data_file)
            writer.writerows(olympic_event_results_list)
        
        return olympic_event_results_list

    def write_per_olympic_athlete_data_csv(self, raw_dictionary):
        '''
        From athlete_events_raw, create an per_olympic_athlete_data_list and write to a csv file.

        Columns in per_olympic_athlete_data_list:
            0   1           2            3    4       5
            ID, Olympic ID, Olympian ID, Age, Height, Weight
        '''
        per_olympic_athlete_data_list = []
        for row in raw_dictionary:
            temp_per_olympic_athlete_data = []
            exists_boolean = False

            for athlete_entry in per_olympic_athlete_data_list:
                if row[0] == athlete_entry[2] and row[3] == athlete_entry[3]:
                    exists_boolean = True
            if exists_boolean is False:
                temp_per_olympic_athlete_data.append(len(per_olympic_athlete_data_list) + 1) # ID
                olympic_id_num = 1

                for olympics in self.olympics:
                        if olympics[1] == row[8]: # Searching for Olympic ID
                            temp_per_olympic_athlete_data.append(olympic_id_num) # Olympic ID
                        else:
                            olympic_id_num = olympic_id_num + 1

                olympian_id_num = 1
                for olympian in self.olympian_athletes:
                        if olympian[0] == row[0]: # Searching for Olympian ID
                            temp_per_olympic_athlete_data.append(olympian_id_num) # Olympian ID
                        else:
                            olympian_id_num = olympian_id_num + 1

                temp_per_olympic_athlete_data.append(row[3]) # Age
                temp_per_olympic_athlete_data.append(row[4]) # Height
                temp_per_olympic_athlete_data.append(row[5]) # Weight
                per_olympic_athlete_data_list.append(temp_per_olympic_athlete_data)

        with open('per_olympic_athlete_data.csv', 'w') as per_olympic_athlete_data_file:
            writer = csv.writer(per_olympic_athlete_data_file)
            writer.writerows(per_olympic_athlete_data_list)

        return per_olympic_athlete_data_list

if __name__ == '__main__':
    olympics = olympic_db('athlete_events.csv', 'noc_regions.csv')

    '''
    Quick Copy Things! AKA Everything is burning down quick, test the things!

    if len(per_olympic_athlete_data_list) >= 10: # Purely for testing. No way I'm sitting through 100k lines of data each time I run this.
                break
    '''