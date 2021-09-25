'''
   booksdatasourcetest.py
   Jeff Ondich, 24 September 2021
'''

'''
Tests to make:
- Test book with number in title
- Test single letter book search
- Test letters with accents author search
- Test dead author
- Test just start year
- Test empty book search
- Test author tie breaking by given name


Tests made:
- Test unique author
- Test unique book
- Test same year

'''

import booksdatasource
import unittest

class BooksDataSourceTester(unittest.TestCase):
    def setUp(self):
        self.data_source = booksdatasource.BooksDataSource('books1.csv')

    def tearDown(self):
        pass

    def test_unique_author(self):
        authors = self.data_source.authors('Pratchett') # Search Term that goes into books.py.
        self.assertTrue(len(authors) == 1) # Sees if authors is an array with length 1.
        self.assertTrue(authors[0] == Author('Pratchett', 'Terry')) # Sees if the first slot in the author array # contains Pratchett and Terry.

    def test_unique_book(self):
        books = self.data_source.books('Never')
        self.assertTrue(len(books) == 1)
        self.assertTrue(books[0] == Book('Neverwhere'))

    def test_startyear_equals_endyear(self):
        books = self.data_source.books_between_years(1939,1939)
        self.assertTrue(len(books) == 1)
        self.assertTrue(books[0] == Book('And Then There Were None'))

if __name__ == '__main__':
    unittest.main()

