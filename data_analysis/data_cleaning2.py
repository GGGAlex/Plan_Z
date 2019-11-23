import pandas as pd
df = pd.read_csv('tmdb_5000_movies_id.csv',names=['id', 'language', 'overview', 'release_date', 'runtime',
       'title', 'vote_average', 'vote_count', 'company', 'country', 'director',
       'genre', 'star', 'writer'])




df.set_index('id', inplace=True)
df.dropna(inplace=True)
df