import warnings
import pandas as pd
import joblib
import csv

warnings.simplefilter('ignore')


class Recommender:
    def __init__(self):
        self.indices = joblib.load('/home/kevin/Documents/9321/github/Plan_Z/ML/indices')
        self.smd = joblib.load('/home/kevin/Documents/9321/github/Plan_Z/ML/smd')
        self.cosine_sim = joblib.load('/home/kevin/Documents/9321/github/Plan_Z/ML/cosine')

    def improved_recommendations(self, title):
        idx = self.indices[title]
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:26]
        movie_indices = [i[0] for i in sim_scores]

        movies = self.smd.iloc[movie_indices][['title', 'vote_count', 'vote_average', 'year']]
        vote_counts = movies[movies['vote_count'].notnull()]['vote_count'].astype('int')
        vote_averages = movies[movies['vote_average'].notnull()]['vote_average'].astype('int')
        C = vote_averages.mean()
        m = vote_counts.quantile(0.60)
        qualified = movies[
            (movies['vote_count'] >= m) & (movies['vote_count'].notnull()) & (movies['vote_average'].notnull())]
        qualified['vote_count'] = qualified['vote_count'].astype('int')
        qualified['vote_average'] = qualified['vote_average'].astype('int')
        qualified['wr'] = qualified.apply(lambda x: (x['vote_count'] /
                                                     (x['vote_count'] + m) * x['vote_average'])
                                                    + (m / (m + x['vote_count']) * C), axis=1)
        qualified = qualified.sort_values('wr', ascending=False).head(10)
        return qualified


# if __name__ == '__main__':
#     csv_file1 = '../data_analysis/tmdb_5000_movies.csv'
#     csv_file2 = '../data_analysis/movies.csv'
#     year_movie_csv = '../data_analysis/movie_of_year.csv'
#     logging_csv = "../logging.csv"
#     # with open(logging_csv,'wb') as f:
#     # 	csv_write = csv.writer(f)
#     # 	csv_head = ["IP_address", "Time", "Function"]
#     # 	csv_write.writerow(csv_head)
#     df1 = pd.read_csv(csv_file1)
#     df2 = pd.read_csv(csv_file2)
#     # logging_df = pd.read_csv(logging_csv)
#     year_movie_df = pd.read_csv(year_movie_csv)
#     year_movie_df.set_index('release_date', inplace=True)
#     df2.rename(columns={'name': 'title'}, inplace=True)
#     df = pd.merge(df1, df2, on='title')
#     df.drop(['budget_x', 'keywords', 'genres', 'homepage', 'id', 'original_title', 'rating', 'gross', \
#              'budget_y', 'spoken_languages', 'runtime_y', 'production_companies', 'revenue', \
#              'production_countries', 'tagline', 'released', 'votes', 'year', 'status', 'score', \
#              'popularity'], axis=1, inplace=True)
#     df.rename(columns={'original_language': 'language', 'runtime_x': 'runtime'}, inplace=True)
#     df.dropna(inplace=True)
#     a = recommender()
#     qu = a.improved_recommendations("Thor: The Dark World")
#     dfToList = qu['title'].tolist()
#     for i in range(5):
#         if dfToList[i] not in list(df['title'].values):
#             print('not in database')
#         movie_df = df.copy()
#         movie = (df.loc[df['title'] == dfToList[i]]).to_json(orient='records')
#         print(movie)
