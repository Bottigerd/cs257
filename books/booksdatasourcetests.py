'''
   booksdatasourcetest.py
   Jeff Ondich, 24 September 2021
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

    def test_book_with_number(self):
        books = self.data_source.books('1')
        self.assertTrue(len(books) == 1)
        self.assertTrue(books[0] == Book('1Q84'))
        
    def test_book_single_letter(self):
        books = self.data_source.books('Q')
        self.assertTrue(len(books) == 1)
        self.assertTrue(books[0] == Book('1Q84'))
    
    def test_author_accent_letter(self):
        authors = self.data_source.authors('Brontë')
        self.assertTrue(len(authors) == 3)

    def test_dead_author(self):
        authors = self.data_source.authors('Willis')
        self.assertTrue(len(authors) == 1)
        self.assertTrue(authors[0] == Author('Willis', 'Connie'))

    def test_start_year_only(self):
        books = self.data_source.books_between_years(2003, 0) #Not sure what value would show that there's no end year. Using 0 for now.
        self.assertTrue(len(books) == 9)

    def test_all_books(self):
        books = self.data_source.books()
        self.assertTrue(len(books) == 41)

    def test_author_accent_letter(self):
        authors = self.data_source.authors('Brontë')
        self.assertTrue(len(authors) == 3)
        self.assertTrue(authors[0] == Author('Brontë', 'Ann'))


if __name__ == '__main__':
    unittest.main()

