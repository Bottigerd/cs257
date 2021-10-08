#!/usr/bin/env python3
'''
    booksdatasource.py
    Dani Bottiger and Kiri Salij

    For use in the "books" assignment at the beginning of Carleton's
    CS 257 Software Design class, Fall 2021.
'''

import csv
import operator

class Author:
    def __init__(self, surname='', given_name='', birth_year=None, death_year=None):
        self.surname = surname
        self.given_name = given_name
        self.birth_year = birth_year
        self.death_year = death_year

    def __eq__(self, other):
        ''' For simplicity, we're going to assume that no two authors have the same name. '''
        return self.surname == other.surname and self.given_name == other.given_name


class Book:
    def __init__(self, title='', publication_year=None, authors=[]):
        ''' Note that the self.authors instance variable is a list of
            references to Author objects. '''
        self.title = title
        self.publication_year = publication_year
        self.authors = authors
        self.primaryAuthor = authors[0] # this is the first author for easy sorting by surname

    def __eq__(self, other):
        ''' We're going to make the excessively simplifying assumption that
            no two books have the same title, so "same title" is the same
            thing as "same book". '''
        return self.title == other.title

class BooksDataSource:
    def __init__(self, books_csv_file_name):
        ''' The books CSV file format looks like this:

                title,publication_year,author_description

            For example:

                All Clear,2010,Connie Willis (1945-)
                "Right Ho, Jeeves",1934,Pelham Grenville Wodehouse (1881-1975)

            This __init__ method parses the specified CSV file and creates
            suitable instance variables for the BooksDataSource object containing
            a collection of Author objects and a collection of Book objects.
        '''
        
        self.booksList = [] # The complete list of books
        self.authorsList = [] # The complete list of authors

        if len(self.booksList) != 0:
            return None
        
        file = open(books_csv_file_name)
        csvreader = csv.reader(file)
        rows = []
        for row in csvreader: 
            rows.append(row)
        file.close()

        for row in rows: # each row in rows is a different book publication
            bookTitle = row[0]
            publicationYear = row[1]
            authorsString = row[2] # this is a string of the author(s) information (pre-parsing)

            '''
            Parsing Author Information
            This should work unless we have an author with three words in their name which is the case sometimes.
            Here's some thoughts on how we could get that to work:
                We could keep concatinating onto the given name/surname until the first character of our string is a '(', in which case we move onto our usual birth/death year stuff. 
                We could probably have an index counter for where we are in authorTemp, so the stuff for second author would be like index+1, index+2, etc.
            '''
            authorTemp = authorsString.split(' ') # this splits our string of authors into an array for easier digesting.
            '''
            Name Parsing, Author 1
            '''
            index = 0
            givenName = ''
            while authorTemp[index+1][0] != '(':
                givenName = givenName + authorTemp[index] + ' '
                index = index + 1
            
            surname = authorTemp[index].strip()
            givenName = givenName.strip()

            '''
            Year Parsing and appending to lists, Author 1
            '''
            birthYearTemp = authorTemp[index+1][1: 5]
            deathYearTemp = None # this creates deathYearTemp so we can access it outside of the if statement
            author1 = None # this creates the author so we can access it outside of the if statement and so we can add it to the book later
            booksAuthors = []
            if len(authorTemp[index+1]) > 7:
                deathYearTemp = authorTemp[index+1][6: 10] # this gets the death year if it does exist
                author1 = Author(surname, givenName, birthYearTemp, deathYearTemp)
            else:
                author1 = Author(surname, givenName, birthYearTemp, '')
            
            if author1 not in self.authorsList:
                self.authorsList.append(author1) # this adds our now parsed author to the list of authors
            
            booksAuthors.append(author1)

            '''
            Name Parsing, Author 2
            '''
            author2 = None # we have a variable so we can add it to the book
            index = index + 3 # one for the years, one for the and that seperates the authors

            if len(authorTemp)-index > 0: # this is for the case of more than one author
                givenName = ''
                while authorTemp[index+1][0] != '(':
                    givenName = givenName + authorTemp[index] + ' '
                    index = index + 1
            
                surname = authorTemp[index].strip()
                givenName = givenName.strip()

                '''
                Year Parsing and appending to lists, Author 2
                '''
                birthYearTemp = authorTemp[index+1][1: 5]
                if len(authorTemp[index+1]) > 7:
                    deathYearTemp = authorTemp[6][6: 10] # this gets the death year if it does exist
                    author2 = Author(surname, givenName, birthYearTemp, deathYearTemp)
                else:
                    author2 = Author(surname, givenName, birthYearTemp, '')
                
                if author1 not in self.authorsList:                
                    self.authorsList.append(author2)
                booksAuthors.append(author2)

            '''
            Parsing Book Information
            '''
            book1 = Book(bookTitle, publicationYear, booksAuthors)
            self.booksList.append(book1)

    def printBooks(self, printedList = []):
        '''
        A method purely for testing if booksList got its information right
        '''

        for book in printedList:
            if (len(book.authors) > 1):
                # title, publication_year, author0.given_name author0.surname (author0.birth_year - author0.death_year)
                # and author1.given_name author1.surname (author1.birth_year - author1.death_year)
                print(book.title + ', ' + book.publication_year + ', ' + book.authors[0].given_name + ' ' + book.authors[0].surname + ' (' + book.authors[0].birth_year + '-' + book.authors[0].death_year + ')' + ' and ' + book.authors[1].given_name + ' ' + book.authors[1].surname+ '(' + book.authors[1].birth_year + '-' + book.authors[1].death_year + ')')
            else:
                # title, publication_year, author0.given_name author0.surname (author0.birth_year - author0.death_year)
                print(book.title + ', ' + book.publication_year + ', ' + book.authors[0].given_name + ' ' + book.authors[0].surname + ' (' + book.authors[0].birth_year + '-' + book.authors[0].death_year + ')')

    def printAuthors(self, printedList = []):
        '''
        A method purely for testing if booksList got its information right
        ''' 
        
        for author in printedList:
            print(author.given_name + ' ' + author.surname + ' (' + author.birth_year + '-' + author.death_year + ')')        

    def authors(self, search_text=None):
        ''' Returns a list of all the Author objects in this data source whose names contain
            (case-insensitively) the search text. If search_text is None, then this method
            returns all of the Author objects. In either case, the returned list is sorted
            by surname, breaking ties using given name (e.g. Ann Brontë comes before Charlotte Brontë).
        '''

        qualifyingauthors = []
        if search_text == None:
            qualifyingauthors = self.booksList
        else:
            for book in self.booksList:
                if search_text.lower() in book.authors[0].surname.lower() or search_text.lower() in book.authors[0].given_name.lower():
                    qualifyingauthors.append(book)
                elif len(book.authors) > 1 and (search_text.lower() in book.authors[1].surname.lower() or search_text.lower() in book.authors[1].given_name.lower()):
                    qualifyingauthors.append(book)

        return self.sortBySurname(qualifyingauthors)

    def books(self, search_text=None, sort_by='title'):
        ''' Returns a list of all the Book objects in this data source whose
            titles contain (case-insensitively) search_text. If search_text is None,
            then this method returns all of the books objects.

            The list of books is sorted in an order depending on the sort_by parameter:

                'year' -- sorts by publication_year, breaking ties with (case-insenstive) title
                'title' -- sorts by (case-insensitive) title, breaking ties with publication_year
                default -- same as 'title' (that is, if sort_by is anything other than 'year'
                            or 'title', just do the same thing you would do for 'title')
        '''
        qualifyingbooks = []
        if search_text==None:
            qualifyingbooks = self.booksList
        else: 
            for book in self.booksList:
                if search_text.lower() in book.title.lower():
                    qualifyingbooks.append(book)
        
        if sort_by == 'year':
            return self.sortByYear(qualifyingbooks)
        else:
            return self.sortByTitle(qualifyingbooks)



    def books_between_years(self, start_year=None, end_year=None):
        ''' Returns a list of all the Book objects in this data source whose publication
            years are between start_year and end_year, inclusive. The list is sorted
            by publication year, breaking ties by title (e.g. Neverwhere 1996 should
            come before Thief of Time 1996).

            If start_year is None, then any book published before or during end_year
            should be included. If end_year is None, then any book published after or
            during start_year should be included. If both are None, then all books
            should be included.
        '''
        qualifyingbooks = []
        
        if start_year != None and end_year != None and start_year > end_year: #in case the order of the years doesn't make sense, we can swap them instead of throwing an error
            temp = start_year
            start_year = end_year
            end_year = temp
        
        if start_year == None and end_year == None:
            qualifyingbooks = self.booksList
        elif start_year == None:
            '''
            Get all the books published from the beginning of time to end_year (inclusive)
            '''
            for book in self.booksList:
                if int(book.publication_year) <= end_year:
                    qualifyingbooks.append(book)
        elif end_year == None:
            '''
            Get all the books published from the start_year to the end of time (inclusive)
            '''
            for book in self.booksList:
                if int(book.publication_year) >= start_year:
                    qualifyingbooks.append(book)
        else:
            '''
            Get all books published between the start_year (inclusive) and end-year (inclusive)
            '''
            for book in self.booksList:
                if int(book.publication_year) >= start_year and int(book.publication_year) <= end_year:
                    qualifyingbooks.append(book)
        
        return self.sortByYear(qualifyingbooks)
    
    def sortByYear(self, qualifyingbooks = []):
        '''
        Sorts a list of given books by their publication date, ties are broken by title.
        '''
        sortedBooks = sorted(qualifyingbooks, key = operator.attrgetter('publication_year', 'title'))
        return sortedBooks

    def sortByTitle(self, qualifyingbooks = []):
        '''
        Sorts a list of given books by their title, breaking ties by year. Though there shouldn't be any books with the same name.
        '''

        sortedBooks = sorted(qualifyingbooks, key = operator.attrgetter('title', 'publication_year'))
        return sortedBooks

    def sortBySurname(self, qualifyingauthors = []):
        '''
        Sorts a list of given authors by their surname, breaking ties by given name.
        '''
        sortedAuthors = sorted(qualifyingauthors, key = operator.attrgetter('primaryAuthor.surname', 'primaryAuthor.given_name'))
        return sortedAuthors
