'''
    books.py
    Dani Bottiger and Kiri Salij

    CS 257 Software Design class, Fall 2021
'''

import argparse
from booksdatasource import Book, Author, BooksDataSource

parser = argparse.ArgumentParser(description='Searches book database', add_help=False)

#arguemnts
parser.add_argument('-a', '--authors', action='store_true', help = 'tag for an author search')
parser.add_argument('-b', '--books', action='store_true', help = 'tag for book search') # technically not used, but just to extra enforce
                                                                                        # to the user that yes they are sorting by books.
parser.add_argument('-r', '--range', action='store_true', help = 'tag for year range search')

parser.add_argument('search_term', metavar = 'search_term', type=str, nargs='?', help = 'search term for books database')
parser.add_argument('search_term2', type=int, nargs='?', help = 'search term for books database')

parser.add_argument('-B', '--book_sort', action='store_true', help = 'tag for a book title sort') # technically not used, but just to extra enforce
                                                                                                 # to the user that yes they are sorting by books.
parser.add_argument('-Y', '--year_sort', action='store_true', help = 'tag for a publication year sort')

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
    search_results = booksdatasource.authors(args.search_term)
    booksdatasource.print_books(search_results)
elif args.range:
    search_results = booksdatasource.books_between_years(args.search_term, args.search_term2)
    booksdatasource.print_books(search_results)
else:
    if args.year_sort:
        search_results = booksdatasource.books(args.search_term, 'year')
    else:
        search_results = booksdatasource.books(args.search_term)
    booksdatasource.print_books(search_results)

# We just wanted the terminal to be a little bit more readable that is all.
print()
print()
