'''
   booksdatasourcetest.py
   Dani Bottiger and Kiri Salij
   CS257 Software Design - Fall 2021
'''
import booksdatasource
from booksdatasource import Author
from booksdatasource import Book
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
        self.assertTrue(authors == 21) 


if __name__ == '__main__':
    unittest.main()

