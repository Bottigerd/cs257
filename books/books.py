#Kiri and Dani books.py
#Version 1 9/28/21

import argparse
from booksdatasource import Book, Author, BooksDataSource

parser = argparse.ArgumentParser(description='Searches book database', add_help=False)

#arguemnts
parser.add_argument('-a', '--authors', action='store_true', help = 'tag for an author search')
parser.add_argument('-b', '--books', action='store_true', help = 'tag for book search') # technically not used, but just to extra enforce
                                                                                        # to the user that yes they are sorting by books.
parser.add_argument('-r', '--range', action='store_true', help = 'tag for year range search')

parser.add_argument('searchTerm', metavar = 'searchTerm', type=str, nargs='?', help = 'search term for books database')
parser.add_argument('searchTerm2', type=int, nargs='?', help = 'search term for books database')

parser.add_argument('-B', '--BookSort', action='store_true', help = 'tag for a book title sort') # technically not used, but just to extra enforce 
                                                                                                 # to the user that yes they are sorting by books.
parser.add_argument('-Y', '--YearSort', action='store_true', help = 'tag for a publication year sort')

parser.add_argument('-h', '--help', action='store_true', help = 'show this help message')

#parsing the arugments
args = parser.parse_args()

#running the search
booksdatasource = BooksDataSource('books1.csv')

if args.help:
    f = open('usage.txt', 'r')
    content = f.read()
    print(content)
    f.close()
elif args.authors:
    searchResults = booksdatasource.authors(args.searchTerm)
    booksdatasource.printBooks(searchResults)
elif args.range:
    searchResults = booksdatasource.books_between_years(args.searchTerm, args.searchTerm2)
    booksdatasource.printBooks(searchResults)
else:
    if args.YearSort:
        searchResults = booksdatasource.books(args.searchTerm, 'year')
    else:
        searchResults = booksdatasource.books(args.searchTerm)
    booksdatasource.printBooks(searchResults)

# We just wanted the terminal to be a little bit more readable that is all.
print()
print()
