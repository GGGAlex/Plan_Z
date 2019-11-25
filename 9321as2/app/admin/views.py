# coding: utf-8
from flask import Flask, request
from flask_restplus import Resource, Api, fields
import pandas as pd
import csv
import json
import joblib

apiApp = Flask(__name__)
api = Api(apiApp)
apiApp.debug = True

# Api start
movie_model = api.model('Movie', {
    'title': fields.String,
    'language': fields.String,
    'overview': fields.String,
    'release_date': fields.String,
    'runtime': fields.Float,
    'vote_average': fields.Float,
    'vote_count': fields.Integer,
    'company': fields.String,
    'country': fields.String,
    'director': fields.String,
    'genre': fields.String,
    'star': fields.String,
    'writer': fields.String,
})

log_model = api.model('log', {
    'IP_address': fields.String,
    'Time': fields.String,
    'Function': fields.String,
})


class Recommender:
    def __init__(self):
        self.indices = joblib.load('indices')
        self.smd = joblib.load('smd')
        self.cosine_sim = joblib.load('cosine')

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


@api.route('/movies/<string:title>')
@api.parm('title', 'The name of movies')
class Movies(Resource):

    @api.response(200, 'Successful')
    @api.doc(description='Get Target Movie')
    def get(self, title):
        if title not in list(df['title'].values):
            api.abort(404, "Movie {} doesn't exist".format(title))
            # add new movie link
        movie_df = df.copy()
        movie = (df.loc[df['title'] == title]).to_json(orient='records')
        return json.loads(movie)

    @api.response(200, 'Successful')
    @api.doc(description='Delete A Movie')
    def delete(self, title):
        if title not in list(df['title'].values):
            api.abort(404, "Movie {} doesn't exist".format(title))
        deleteMovie = df[df['title'] == title].index

        # Delete these row indexes from dataFrame
        df.drop(deleteMovie, inplace=True)
        return {"message": "Movie {} is removed.".format(title)}


@api.route('/movies/logging')
class writeLogging(Resource):
    @api.doc(description='Record logging file')
    @api.expect(log_model)
    def post(self):
        message = request.json
        print(message)
        new_data = [message['IP_address'], message['Time'], message['Function']]
        colNames = logging_df.columns
        new_log_df = pd.DataFrame(data=[new_data], columns=colNames)
        complete_logging_df = pd.concat([logging_df, new_log_df], axis=0)
        complete_logging_df.to_csv(logging_csv, index=False)
        return {"message": "logging is update."}, 200


@api.route('/movies')
class getMovies(Resource):
    def get(self):
        movies = df.to_json(orient='records')
        return json.loads(movies)

    @api.doc(description='Post new movies')
    @api.expect(movie_model)
    def post(self):
        movie = request.json

        if 'title' not in movie:
            return {"message": "Missing Identifier"}, 400

        movie_title = movie['title']

        # check if the given identifier does not exist
        if movie_title in df.title:
            return {"message": "{} is already in the dataset".format(movie_title)}, 400

        # Put the values into the dataframe
        for key in movie:
            if key not in movie_model.keys():
                # unexpected column
                return {"message": "Property {} is invalid".format(key)}, 400
            df.loc[movie_title, key] = movie[key]

        # df.append(book, ignore_index=True)
        return {"message": "Movie {} is created".format(movie_title)}, 201
        # return{'hello':'world'}

@api.route('/movies/analysis/top5movies')
class getTopMovies(Resource):
    def get(self):
        df['release_date'] = df['release_date'].str.replace('-', '')
        df['release_date'] = df['release_date'].map(lambda x: int(x)//10000)
        movie_of_year = df.groupby('release_date', group_keys=False).apply(lambda x: x.sort_values('vote_average',ascending=False))\
                    .groupby('release_date').head(5)
        movie_of_year.drop(['overview', 'writer', 'star', 'runtime', 'company',
                        'genre', 'vote_count'], axis=1, inplace=True)
        movie_of_year = movie_of_year[movie_of_year.release_date>2005].reset_index()
        movie_of_year.drop(['index'], axis=1, inplace=True)
        #movie_of_year = movie_of_year.groupby(by='release_date')
        #topmovie = movie_of_year.to_json()
        topmovie = movie_of_year.to_json(orient='records')
        return json.loads(topmovie)

@api.route('/movies/analysis/general')
class getMovietypes(Resource):
    def get(self):
        types = df.copy()
        types = types['genre'].value_counts().reset_index(name='count')
        types.rename(columns={'index': 'genre'}, inplace=True)
        typemovie = types.to_json(orient='records')
        return json.loads(typemovie)


@api.route('/movies/analysis/best_movie_year/<int:year>')
@api.parm('year', 'The Target year')
class getYearMovies(Resource):

    @api.response(200, 'Successful')
    def get(self, year):
        if year not in year_movie_df.index:
            api.abort(404, "Movie {} doesn't exist".format(year))
            # add new movie link
        movie = df.loc[year].to_json()
        # add new movie link
        return movie


@api.route('/movies/analysis/best_movie_year/')
class yearMovies(Resource):
    def get(self):
        movie = year_movie_df.to_json(orient='records')
        return json.loads(movie)


@api.route('/movies/analysis/country/<string:year>')
@api.parm('year', 'The Target year')
class analysisCountry(Resource):
    def get(self, year):
        country = df.copy()
        country['release_date'] = country['release_date'].map(lambda x: x.split("-")[0])
        if year not in list(country['release_date'].values):
            api.abort(404, "Year {} doesn't exist in database".format(year))
        country.set_index('release_date', inplace=True)
        country = country.loc[str(year)]
        country = country.groupby('release_date')['country'].value_counts().reset_index(name='country_count')
        country.drop(['release_date'], axis=1, inplace=True)
        country.set_index('country', inplace=True)
        dfjson = country.to_json()
        return json.loads(dfjson)


@api.route('/movies/analysis/country')
class getCountryNum(Resource):
    @api.doc(description='Count movies by country')
    def get(self):
        country = df.copy()
        country = country['country'].value_counts().reset_index(name='country_count')
        country.rename(columns={'index': 'country'}, inplace=True)
        dfjson = country[:4].to_json(orient='records')
        return json.loads(dfjson)


@api.route('/recommand/<string:title>')
@api.parm('title', 'Name of movies')
class recommandMovie(Resource):

    @api.doc(description='Make recomandation')
    def get(self, title):
        a = Recommender()
        qu = a.improved_recommendations(title)
        dfToList = qu['title'].tolist()
        s = "["
        for i in range(5):
            if dfToList[i] not in list(df['title'].values):
                continue
            movie = (df.loc[df['title'] == dfToList[i]]).to_json(orient='records')
            s += movie[1:-2] + "},\n"
        s = s[:-2] + "]"
        return json.loads(s)


# Api end

if __name__ == '__main__':
    csv_file1 = '../data_analysis/tmdb_5000_movies.csv'
    csv_file2 = '../data_analysis/movies.csv'
    year_movie_csv = '../data_analysis/movie_of_year.csv'

    logging_csv = "../data_analysis/logging.csv"

    with open(logging_csv, 'w') as f:
        csv_write = csv.writer(f)
        csv_head = ["IP_address", "Time", "Function"]
        csv_write.writerow(csv_head)

    df1 = pd.read_csv(csv_file1)
    df2 = pd.read_csv(csv_file2)
    logging_df = pd.read_csv(logging_csv)
    year_movie_df = pd.read_csv(year_movie_csv)

    # year_movie_df.set_index('release_date', inplace=True)

    df2.rename(columns={'name': 'title'}, inplace=True)
    df = pd.merge(df1, df2, on='title')
    df.drop(['budget_x', 'keywords', 'genres', 'homepage', 'id', 'original_title', 'rating', 'gross', \
             'budget_y', 'spoken_languages', 'runtime_y', 'production_companies', 'revenue', \
             'production_countries', 'tagline', 'released', 'votes', 'year', 'status', 'score', \
             'popularity'], axis=1, inplace=True)
    df.rename(columns={'original_language': 'language', 'runtime_x': 'runtime'}, inplace=True)
    # df.rename(columns={'original_language': 'language','runtime_x': 'runtime'}, inplace=True)

    # df.set_index('title', inplace=True)
    df.dropna(inplace=True)
    apiApp.run(port=5000)
