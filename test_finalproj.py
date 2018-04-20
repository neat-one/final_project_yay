import unittest
from nflproj import *

class TestDatabase(unittest.TestCase):

    def test_top_movies(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT Title FROM Movies'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Moana',), result_list)
        self.assertGreater(len(result_list), 99)

        sql = '''
            SELECT Title
            FROM Movies
            WHERE imdbRating > 7
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertGreater(len(result_list), 68)
        self.assertEqual(result_list[0], ('The Godfather',))

        conn.close()

    def test_details(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
            SELECT MovieID
            FROM Details
            WHERE Comments > 4
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('82',), result_list)
        self.assertGreater(len(result_list), 15)

        sql = '''
            SELECT COUNT(*)
            FROM Details
        '''
        results = cur.execute(sql)
        count = results.fetchone()[0]
        self.assertGreater(count, 99)

        conn.close()

    def test_joins(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
            SELECT imdbID
            FROM Details
                JOIN Movies
                ON Details.MovieID = Movies.ID
            WHERE Comments = 0
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('tt1340800',), result_list)
        conn.close()

class TestOMDBFunction(unittest.TestCase):

    def test_problem01(self):
        example = getOMDBData("Moana")
        self.assertTrue('Title' in example)
        self.assertTrue('Runtime' in example)
        self.assertTrue('imdbRating' in example)
        self.assertTrue('Plot' in example)

class TestDeviantArtFunction(unittest.TestCase):

    def test_it(self):
        results = get_deviant('The Godfather')
        self.assertTrue(results != None)
        self.assertTrue(type(results) == int)

unittest.main()
