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

    def test_different_years(self):
        books = self.data_source.books_between_years(2018,2019)
        self.assertTrue(len(books) == 2)
        self.assertTrue(books[0] == Book('There, There'))
        self.assertTrue(books[1] == Book('Fine, Thanks'))

    def test_comma_in_book(self):
        books = self.data_source.books(',')
        self.assertTrue(len(books) == 4)
        self.assertTrue(books == ['Fine, Thanks','Right Ho, Jeeves','The Life and Opinions of Tristram Shandy, Gentleman','There, There'])
        #might need to change the format of the above line because I am unsure how python checks equivalency between lists

    def test_startyear_earlier_than_endyear(self):
        books = self.data_source.books_between_years(2019,2018)
        self.assertTrue(len(books) == 41)
        #honestly not sure what the desired outcome of this test should be, I think it depends on how we want to implement books_between_years

    def test_multiple_authors_one_book(self):
        books = self.data_source.books('Good Omens')
        self.assertTrue(len(books[0].authors) == 2)

    def test_alive_author(self):
        authors = self.data_source.authors('Morrison')
        self.assertTrue(len(authors) == 1) #okay so I'm not sure whether the length of authors actually should be 2 because Toni Morrison wrote 2 books but she herself is only 1 author
        self.assertTrue(authors[0] == Author('Morrison','Toni'))

    def test_endyear_only(self):
        books = self.data_source.books_between_years(None,1813)
        self.assertTrue(len(books) == 3)
        self.assertTrue(books[0] == Book('The Life and Opinions of Tristram Shandy, Gentleman'))

    def test_empty_author(self):
        authors = self.data_source.authors()
        self.assertTrue(authors == []) #yes this test will already pass but I'm not sure what else we would want an empty search to output

if __name__ == '__main__':
    unittest.main()

