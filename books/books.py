#Kiri and Dani books.py
#Version 1 9/28/21

import argparse
from booksdatasource import Book, Author, BooksDataSource

parser = argparse.ArgumentParser(description='Searches book database')

#arguemnts
parser.add_argument('-a', '--authors', action='store_true', help = 'tag for an author search')
parser.add_argument('-b', '--books', action='store_true', help = 'tag for book search')
parser.add_argument('-r', '--range', action='store_true', help = 'tag for year range search')

parser.add_argument('searchTerm', metavar = 'searchTerm', type=str, nargs='?', help = 'search term for books database')

parser.add_argument('startYear', type=int, nargs='?', default = 0, help = 'start year for books database')
parser.add_argument('endYear', type=int, nargs='?', default = 0, help = 'end year for books database')

parser.add_argument('-B', '--BookSort', action='store_true', help = 'tag for a book title sort')
parser.add_argument('-Y', '--YearSort', action='store_true', help = 'tag for a publication year sort')

#parsing the arugments
args = parser.parse_args()

#running the search
booksdatasource = BooksDataSource('books1.csv')

if args.authors:
    searchResults = booksdatasource.authors(args.searchTerm)
    booksdatasource.printAuthors(searchResults)
elif args.books:
    if args.YearSort:
        searchResults = booksdatasource.books(args.searchTerm, 'year')
    else:
        searchResults = booksdatasource.books(args.searchTerm)
    booksdatasource.printBooks(searchResults)
elif args.range:
    searchResults = booksdatasource.books_between_years(args.startYear, args.endYear)
    booksdatasource.printBooks(searchResults)
else:
    if args.YearSort:
        searchResults = booksdatasource.books(args.searchTerm, 'year')
    else:
        searchResults = booksdatasource.books(args.searchTerm)
    booksdatasource.printBooks(searchResults)
