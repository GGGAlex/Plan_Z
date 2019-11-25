import pandas as pd


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


def type_of_movie():
    movie_type = df.groupby(by='genre')['title'].count()
    type_of_movie = movie_type.to_frame()
    type_of_movie.rename(columns={'title':'number'}, inplace=True)
    print(type_of_movie)

#df.set_index('title', inplace=True)
df.dropna(inplace=True)
print(df.to_string())
df.to_csv("movie_data.csv")

type_of_movie()
