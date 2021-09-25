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
        authors = self.data_source.authors('Pratchett')
        self.assertTrue(len(authors) == 1)
        self.assertTrue(authors[0] == Author('Pratchett', 'Terry'))

    def test_startyear_equals_endyear(self):
        books = self.data_source.books_between_years(1939,1939)
        self.assertTrue(len(books) == 1)
        self.assertTrue(books[0] == Book('And Then There Were None')

if __name__ == '__main__':
    unittest.main()

