#Kiri and Dani books.py
#Version 1 9/28/21

import argparse
from booksdatasource import Book, Author, BooksDataSource

parser = argparse.ArgumentParser(description='Searches book database')

#arguemnts
parser.add_argument('searchTerm', metavar = 'searchTerm', type=str, help = 'search term for books database')

#parsing the arugments
args = parser.parse_args()

#running the search
books = BooksDataSource('books1.csv')

searchResults = books.books(args.searchTerm)
books.printBooks(searchResults)