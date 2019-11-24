import pandas as pd
import matplotlib.pyplot as plt

csv_file1 = 'tmdb_5000_movies.csv'
csv_file2 = 'movies.csv'

df1 = pd.read_csv(csv_file1)
df2 = pd.read_csv(csv_file2)

df2.rename(columns={'name': 'title'}, inplace=True)
df = pd.merge(df1, df2, on='title')
df.drop(['budget_x','keywords','genres','homepage','id','original_title','rating','gross',\
         'budget_y','spoken_languages','runtime_y','production_companies','revenue',\
         'production_countries','tagline','released','votes','year','status','score',\
         'popularity'], axis=1, inplace=True)
df.rename(columns={'original_language': 'language','runtime_x': 'runtime'}, inplace=True)

#df.set_index('title', inplace=True)
df.dropna(inplace=True)

def movie_of_year(year):
    # 2006 - 2016
    df['release_date'] = df['release_date'].str.replace('-', '')
    df['release_date'] = df['release_date'].map(lambda x: int(x)//10000)
    movie_of_year = df.groupby('release_date', group_keys=False).apply(lambda x: x.sort_values('vote_average',ascending=False))\
        .groupby('release_date').head(5)
    movie_of_year.drop(['overview', 'writer', 'star', 'runtime', 'company',
                        'genre', 'vote_count'], axis=1, inplace=True)
    movie_of_year = movie_of_year[movie_of_year.release_date>2005].reset_index()
    movie_of_year.drop(['index'], axis=1, inplace=True)
    movie_of_year = movie_of_year.groupby(by='release_date')
    print(movie_of_year.get_group(year).to_string())
    #movie_of_year.to_csv('movie_of_year.csv')

def language_of_year():
    #2010 - 2016

    language_count = df.groupby(by=['release_date','language'])['language'].count()
    language_of_year = language_count[-27:]
    ax = language_of_year.plot.bar()
    plt.show()
    fig = ax.get_figure()
    #fig.savefig('language_of_year.png')
    #print(language_of_year)

def movie_of_country():
    # 2013-2016

    country_count = df.groupby(by=['release_date','country'])['country'].count()
    movie_of_country = country_count[-37:]
    ax = movie_of_country.plot.bar()
    fig = ax.get_figure()
    #fig.savefig('movie_of_year.png')
    plt.show()

    #print(movie_of_country)

def type_of_movie():
    movie_type = df.groupby(by='genre')['title'].count()
    type_of_movie = movie_type.to_frame()
    type_of_movie.rename(columns={'title':'number'}, inplace=True)
    print(type_of_movie)


year = input('please input a year(2006-2016):')
movie_of_year(int(year))
language_of_year()
movie_of_country()
type_of_movie()