import requests
import json
import sqlite3
from secrets import client_id
from secrets import client_secret
from secrets import OMDB_API_KEY
import sys
import plotly.plotly as py
import plotly.graph_objs as go

CACHE_DICT = 'cache.json'
try:
    fref = open(CACHE_NAME, 'r')
    data = fref.read()
    CACHE_DICT = json.loads(data)
    fref.close()

except:
    CACHE_DICT = {}

def get_data_using_cache(url,param=None):
    if param==None:
        unique_identifier=url
        if url in CACHE_DICT:
            print('Getting from cache...')
            return CACHE_DICT[unique_identifier]
        else:
            print("Requesting new data...")
            resp=requests.get(url)
            CACHE_DICT[unique_identifier]=resp.text
            fref=open('cache_data.json','w')
            dumped_data=json.dumps(CACHE_DICT)
            fref.write(dumped_data)
            fref.close()
            return CACHE_DICT[unique_identifier]
    else:
        unique_identifier=url+str(param)
        if unique_identifier in CACHE_DICT:
            print('Getting from cache...')
            return CACHE_DICT[unique_identifier]
        else:
            print("Requesting new data...")
            resp=requests.get(url,param)
            CACHE_DICT[unique_identifier]=json.loads(resp.content.decode('utf-8'))
            fref=open('cache_data.json','w')
            dumped_data=json.dumps(CACHE_DICT)
            fref.write(dumped_data)
            fref.close()
            return CACHE_DICT[unique_identifier]

def auth():
    request = 'https://www.deviantart.com/oauth2/token'
    params = {
        'grant_type' : 'client_credentials',
        'client_id': int(client_id),
        'client_secret': client_secret
    }
    r = get_data_using_cache(request, params)
    return r

def get_deviant(movie_title):
    try:
        request = 'https://www.deviantart.com/api/v1/oauth2/browse/popular'
        params = {
            'q' : movie_title,
            'access_token': auth()['access_token']
        }
        r = get_data_using_cache(request, params)['results'][0]['stats']['comments']
        return r
    except:
        return 0

DBNAME = 'MovieStuff.db'

top_movies = ['The Godfather',  'The Shawshank Redemption',  'Pulp Fiction', \
 'Transformers', 'Up', 'Moana', 'Cinderella', 'Captain America', 'Shrek', \
 'Shrek 2', 'Toy Story', 'Toy Story 2', 'Toy Story 3', 'High School Musical', \
 'High School Musical 2', 'High School Musical 3', 'Spirited Away', \
 "The King's Speech", 'The Lord of the Rings', 'Slumdog Millionaire', \
 'Pokemon', 'Star Wars', 'Saving Private Ryan', 'Interstellar', 'Camp Rock',\
 'Rocky', 'Creed', 'Waking Ned Devine', '12 Angry Men', 'Ghostbusters', \
 'Where the Red Fern Grows', 'Pokemon 2000', 'March of the Penguins',\
  'The Hunger Games', 'Silver Linings Playbook', 'The Jungle Book', 'Finding Nemo',\
  'Finding Dory', 'Monsters, Inc.', 'Monsters University', 'Spirit', 'Tarzan', 'Up',\
  'Mulan', 'Shrek the Third', 'Shrek 2', 'Midnight in Paris', "Breakfast at Tiffany's",\
  'Tinker Tailor Soldier Spy', 'Atomic Blonde', 'Limitless', 'Sing', "Charlotte's Web",\
  'The Hangover', 'Superbad', 'Hercules', 'The Aristocats', 'Lady and the Tramp',\
  'The Fox and the Hound', 'The Iron Giant', 'Boss Baby',
  'Inception', 'Legally Blonde', 'Batman Begins', 'The Brave Little Toaster',\
 'Another Cinderella Story', 'Enchanted', 'Ella Enchanted', 'El Dorado',\
 'Dead Poets Society', 'Meet the Parents', 'Meet the Fockers', 'Emoji Movie',\
 'All Dogs Go to Heaven', 'Hotel for Dogs', 'Madagascar', 'GoodFellas', 'Kill Bill', \
 'Tropic Thunder', 'To Kill a Mockingbird', 'Field of Dreams', 'The Rookie', \
 'The Bee Movie', 'Lincoln', 'The Rugrats Movie', 'Evan Almighty', 'Casino',\
 'Blackfish', 'Kung Fu Panda', 'Chicken Run', 'Antz', 'Nacho Libre', 'Leap', \
 'Casper', 'Up in the Air', '8 Mile', 'The Hurt Locker', 'Dallas Buyers Club',\
 'Coraline', 'Rudy']


def getOMDBData(title):
    response = requests.get('http://www.omdbapi.com', params = {
        'apikey': OMDB_API_KEY,
        't': title
    })
    info = json.loads(response.text)
    return info

def init_first_db():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    statement = '''
        DROP TABLE IF EXISTS "Movies";
    '''
    cur.execute(statement)
    conn.commit()
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = '''
        CREATE TABLE "Movies" (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'imdbID' INTEGER,
            'Title' TEXT,
            'RunTime' INTEGER,
            'imdbRating' INTEGER,
            'MetaScore' INTEGER
        );
    '''
    cur.execute(statement)
    conn.commit()
    conn.close()

def insert_data(dicts):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    insertion = (None, dicts['imdbID'], dicts['Title'], dicts['Runtime'], dicts['imdbRating'], dicts['Metascore'])
    statement = 'INSERT INTO "Movies" '
    statement += 'VALUES (?, ?, ?, ?, ?, ?)'
    cur.execute(statement, insertion)

    conn.commit()
    conn.close()

def init_table3():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    statement = '''
        DROP TABLE IF EXISTS "Details";
    '''
    cur.execute(statement)
    conn.commit()
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = '''
        CREATE TABLE "Details" (
            'MovieID' TEXT,
            'Title' TEXT,
            'Comments' INTEGER
        );
    '''
    cur.execute(statement)
    conn.commit()
    conn.close()

def insert_data2():
    conn=sqlite3.connect(DBNAME)
    cur=conn.cursor()
    query='''
        SELECT Id, Title
        FROM Movies
    '''
    cur.execute(query)
    #conn.commit()
    titles=[]
    #three_inserts = []
    for row in cur:
        titles += [(row[0], row[1])]
    # for x in titles:
    #     comment_number = deviant_comments(get_deviant(x[1]))
    #     three_inserts += [(x[0], x[1], str(comment_number))]
    for x in titles:
        insertion=(x[0], x[1], get_deviant(x[1]))
        statement='INSERT INTO "Details" '
        statement+='VALUES (?, ?, ?)'
        cur.execute(statement, insertion)
    conn.commit()
    conn.close()

class MoreInfo:
    def __init__(self, title):
        try:
            dict_movie = getOMDBData(title)
        except:
            print('No data given on that movie.')
        try:
            self.plot = dict_movie['Plot']
        except:
            self.plot = 'No plot given.'
        try:
            self.release_date = dict_movie['Released']
        except:
            self.release_date = 'No release date given.'
        try:
            self.genre = dict_movie['Genre']
        except:
            self.genre = 'No genre given.'
        try:
            self.director = dict_movie['Director']
        except:
            self.director = 'No director given.'
        try:
            self.actors = dict_movie['Actors']
        except:
            self.actors = 'No actors given.'

def interactive(top_movies):
    counter = 0
    while True:
        user_input2 = input("Would you like to add another title, get graphs, more info, or exit? Enter 'title', 'graphs', 'more' or 'exit'. ")
        if user_input2 == 'exit':
            break
        elif user_input2 == "title":
            user_input3 = input('Enter a movie title: ')
            try:
                if user_input3 not in top_movies:
                    insert_data(getOMDBData(user_input3))
                    print('Movie information added to database for ' + user_input3)
                    top_movies += [user_input3]
                    continue
                else:
                    print('That movie is already in the database. ')
            except:
                print('Please enter a valid movie title')
            if user_input3 == 'exit':
                break
        elif user_input2 == 'graphs':
            graph_object = input('Would you like to see a graph of runtimes, comments, or ratings? ')
            if graph_object == 'runtimes':
                run_type = input('Would you like to compare 2 runtimes? Type "compare". ')
                if run_type == 'compare':
                    for x in top_movies:
                        print(x)
                    graph_variable1 = input('Choose the first movie to compare. ')
                    graph_variable2 = input('Choose the second movie to compare. ')
                    if graph_variable1 in top_movies and graph_variable2 in top_movies:
                        conn=sqlite3.connect(DBNAME)
                        cur=conn.cursor()
                        statement = '''
                            SELECT RunTime
                            FROM Movies
                            WHERE Title = (?)
                        '''
                        graph_variable_end1 = graph_variable1
                        cur.execute(statement, (graph_variable_end1,))
                        run1 = ''
                        for row in cur:
                            run1 = row[0]
                        run_time1 = ''
                        for x in run1:
                            if x.isalpha() == True:
                                pass
                            else:
                                run_time1 += x
                        run_time1 = int(run_time1)

                        statement = '''
                            SELECT RunTime
                            FROM Movies
                            WHERE Title = (?)
                        '''
                        graph_variable_end2 = graph_variable2
                        cur.execute(statement, (graph_variable_end2,))
                        run2 = ''
                        for row in cur:
                            run2 = row[0]
                        run_time2 = ''
                        for x in run2:
                            if x.isalpha() == True:
                                pass
                            else:
                                run_time2 += x
                        try:
                            run_time2 = int(run_time2)
                        except:
                            run_time2 = run_time2
                        conn.close()
                        trace1 = go.Bar(
                        x = [graph_variable1],
                        y = run_time1,
                        name = graph_variable1
                        )
                        trace2 = go.Bar(
                            x=[graph_variable2],
                            y= run_time2,
                            name = graph_variable2
                        )
                        data = [trace1, trace2]
                        layout = go.Layout(
                            barmode ='group',
                            title = 'Movie Runtimes',
                            xaxis=dict(
                        title = 'Title',
                        titlefont=dict(
                            family='Courier New, monospace',
                            size=18,
                            color='#7f7f7f'
                        )), yaxis=dict(
                        title = 'Minutes',
                        titlefont=dict(
                            family='Courier New, monospace',
                            size=18,
                            color='#7f7f7f')))
                        fig = go.Figure(data=data, layout=layout)
                        py.plot(fig, filename='grouped-bar')

                    else:
                        print('You did not enter a title in the list, please start again. ')
                        continue
                else:
                    print('Please try again and enter a valid command. ')
                    continue
            elif graph_object == 'ratings':
                rating_type = input('Would you like to compare 2 movie ratings or look at multiple ratings for 1 movie? Type "compare" or "distribution". ')
                if rating_type == 'compare':
                    for x in top_movies:
                        print(x)
                    graph_variable1 = input('Choose the first movie to compare. ')
                    graph_variable2 = input('Choose the second movie to compare. ')
                    if graph_variable1 in top_movies and graph_variable2 in top_movies:
                        conn=sqlite3.connect(DBNAME)
                        cur=conn.cursor()
                        statement = '''
                            SELECT imdbRating
                            FROM Movies
                            WHERE Title = (?)
                        '''
                        graph_variable_end1 = graph_variable1
                        cur.execute(statement, (graph_variable_end1,))
                        run1 = ''
                        for row in cur:
                            rating1 = row[0]
                        statement = '''
                            SELECT imdbRating
                            FROM Movies
                            WHERE Title = (?)
                        '''
                        graph_variable_end2 = graph_variable2
                        cur.execute(statement, (graph_variable_end2,))
                        run2 = ''
                        for row in cur:
                            rating2 = row[0]
                        conn.close()
                        trace1 = go.Bar(
                        x = [graph_variable1],
                        y = rating1,
                        name = graph_variable1
                        )
                        trace2 = go.Bar(
                            x=[graph_variable2],
                            y= rating2,
                            name = graph_variable2
                        )
                        data = [trace1, trace2]
                        layout = go.Layout(
                            barmode ='group',
                            title = 'IMDB Ratings',
                            xaxis=dict(
                        title = 'Title',
                        titlefont=dict(
                            family='Courier New, monospace',
                            size=18,
                            color='#7f7f7f'
                        )), yaxis=dict(
                        title = 'Score',
                        titlefont=dict(
                            family='Courier New, monospace',
                            size=18,
                            color='#7f7f7f')))
                        fig = go.Figure(data=data, layout=layout)
                        py.plot(fig, filename='grouped-bar')

                    else:
                        print('You did not enter a title in the list, please start again. ')
                        continue
                elif rating_type == 'distribution':
                    for x in top_movies:
                        print(x)
                    graph_variable1 = input('Choose the movie to examine. ')
                    if graph_variable1 in top_movies:
                        conn=sqlite3.connect(DBNAME)
                        cur=conn.cursor()
                        statement = '''
                            SELECT imdbRating, MetaScore
                            FROM Movies
                            WHERE Title = (?)
                        '''
                        graph_variable_end1 = graph_variable1
                        cur.execute(statement, (graph_variable_end1,))
                        run1 = ''
                        for row in cur:
                            rating1 = row[0]
                            try:
                                rating2 = ((float(row[1]))/10.0)
                            except:
                                print('This movie does not have ratings. Please start again and try another. ')
                                continue
                        conn.close()
                        trace1 = go.Bar(
                        x = ['imdbRating'],
                        y = rating1,
                        name = 'imdbRating'
                        )
                        trace2 = go.Bar(
                            x=['MetaScore Rating'],
                            y= rating2,
                            name = 'MetaScore Rating'
                        )
                        data = [trace1, trace2]
                        layout = go.Layout(
                            barmode ='group',
                            title = 'Ratings',
                            xaxis=dict(
                        title = graph_variable1,
                        titlefont=dict(
                            family='Courier New, monospace',
                            size=18,
                            color='#7f7f7f'
                        )), yaxis=dict(
                        title = 'Score',
                        titlefont=dict(
                            family='Courier New, monospace',
                            size=18,
                            color='#7f7f7f')))
                        fig = go.Figure(data=data, layout=layout)
                        py.plot(fig, filename='grouped-bar')

                    else:
                        print('You did not enter a title in the list, please start again. ')
                        continue
            elif graph_object == 'comments':
                for x in top_movies:
                    print(x)
                graph_variable1 = input('Choose the first movie to compare. ')
                graph_variable2 = input('Choose the second movie to compare. ')
                if graph_variable1 in top_movies and graph_variable2 in top_movies:
                    conn=sqlite3.connect(DBNAME)
                    cur=conn.cursor()
                    statement = '''
                        SELECT Comments
                        FROM Details
                            JOIN Movies
                            ON Movies.Id = Details.MovieID
                        WHERE Movies.Title = (?)
                    '''
                    graph_variable_end1 = graph_variable1
                    cur.execute(statement, (graph_variable_end1,))
                    run1 = ''
                    for row in cur:
                        rating1 = row[0]

                    statement = '''
                        SELECT Comments
                        FROM Details
                            JOIN Movies
                            ON Movies.Id = Details.MovieID
                        WHERE Movies.Title = (?)
                    '''
                    graph_variable_end2 = graph_variable2
                    cur.execute(statement, (graph_variable_end2,))
                    run2 = ''
                    for row in cur:
                        run2 = row[0]
                    run_time2 = run2
                    #run_time2 = int(run_time2)
                    conn.close()
                    trace1 = go.Bar(
                    x = [graph_variable1],
                    y = rating1,
                    name = graph_variable1
                    )
                    trace2 = go.Bar(
                        x=[graph_variable2],
                        y= run_time2,
                        name = graph_variable2
                    )
                    data = [trace1, trace2]
                    layout = go.Layout(
                        barmode ='group',
                        title = 'DeviantArt Comments',
                        xaxis=dict(
                    title = 'Title',
                    titlefont=dict(
                        family='Courier New, monospace',
                        size=18,
                        color='#7f7f7f'
                    )), yaxis=dict(
                    title = 'Number of Comments',
                    titlefont=dict(
                        family='Courier New, monospace',
                        size=18,
                        color='#7f7f7f')))
                    fig = go.Figure(data=data, layout=layout)
                    py.plot(fig, filename='grouped-bar')

                else:
                    print('You did not enter a title in the list, please start again. ')
                    continue

            else:
                print('Start over and try again. Use only commands in the info list.')
                continue
        elif user_input2 == 'more':
            movie_name = input('Please enter a title to get more info about. ')
            try:
                name = MoreInfo(movie_name)
            except:
                print('That is not a valid title. Please start again.')
                continue
            data_list = ['plot', 'release date', 'genre', 'director', 'actors']
            print('Info Types:')
            counting = 1
            for x in data_list:
                print(str(counting) + '. '+ x)
                counting += 1
            data_type = input('Please enter all info types you would like to see. ')
            if 'plot' in data_type:
                try:
                    print('Plot: ' + name.plot)
                except:
                    print('There is no plot available.')
            if 'release date' in data_type:
                try:
                    print('Release Date: ' +name.release_date)
                except:
                    print('There is no release_date available.')
            if 'genre' in data_type:
                try:
                    print('Genre: ' + name.genre)
                except:
                    print('There is no genre available.')
            if 'director' in data_type:
                try:
                    print('Director: ' +name.director)
                except:
                    print('There is no director available.')
            if 'actors' in data_type:
                try:
                    print('Actors: ' +name.actors)
                except:
                    print('There are no actors available.')
            if 'plot' not in data_type and 'release date' not in data_type and \
            'genre' not in data_type and 'director' not in data_type and 'actors' not in data_type:
                print('Start over and try again. Use only commands in the info list.')
        else:
            print('Please try again and enter a valid command. ')
            continue
__name__ == "__main__"


if __name__ == "__main__":
    init_first_db()
    init_table3()
    for x in top_movies:
        insert_data(getOMDBData(x))
    insert_data2()
    interactive(top_movies)
