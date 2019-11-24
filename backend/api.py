import pandas as pd
from flask import Flask
from flask import request
import json
from flask_restplus import Api,Resource,fields
app = Flask(__name__)
api = Api(app)
# ['language', 'overview', 'release_date', 'runtime', 'title',
#        'vote_average', 'vote_count', 'company', 'country', 'director', 'genre',
#        'star', 'writer']
movie_model = api.model('Movie', {
    'title': fields.String,
    'language': fields.String,
    'overview': fields.String,
    'release_date': fields.String,
    'runtime': fields.Float,
    'vote_average': fields.Float,
    'vote_count': fields.Integer,
    'company':fields.String, 
    'country':fields.String, 
    'director':fields.String, 
    'genre':fields.String,
    'star':fields.String, 
    'writer':fields.String,
})
@api.route('/movies/<string:title>')
class Movies(Resource):
    def get(self,title):
        if title not in df.index:
            api.abort(404,"Movie {} doesn't exist".format(title))
            #add new movie link
        movie = dict(df.loc[title])
        #add new movie link
        return movie
    def delete(self,title):
        if title not in df.index:
            api.abort(404, "Movie {} doesn't exist".format(title))
        df.drop(title,inplace=True)
        return {"message":"Movie {} is removed.".format(title)}

@api.route('/movies')
class getMovies(Resource):
    def get(self):
        movies = df.to_json(orient='records')
        return json.loads(movies)
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
@api.route('/movies/analysis')
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
# @api.route('/movies/analysis/<int:year>')
# class getYearMovies(Resource):
#     def get(self,year):
#         if year not in year_movie_df.index:
#             api.abort(404,"Movie {} doesn't exist".format(year))
#             #add new movie link
#         movie = df.loc[year].to_json()
#         #add new movie link
#         return movie
#         #add a link to movie page?


if __name__ == '__main__':
    csv_file1 = '/home/kevin/Documents/9321/github/Plan_Z/data_analysis/tmdb_5000_movies.csv'
    csv_file2 = '/home/kevin/Documents/9321/github/Plan_Z/data_analysis/movies.csv'
    year_movie_csv = '/home/kevin/Documents/9321/github/Plan_Z/data_analysis/movie_of_year.csv'
    
    df1 = pd.read_csv(csv_file1)
    df2 = pd.read_csv(csv_file2)
    year_movie_df = pd.read_csv(year_movie_csv)
   
    year_movie_df.set_index('release_date', inplace=True)

    df2.rename(columns={'name': 'title'}, inplace=True)
    df = pd.merge(df1, df2, on='title')
    df.drop(['budget_x','keywords','genres','homepage','id','original_title','rating','gross',\
         'budget_y','spoken_languages','runtime_y','production_companies','revenue',\
         'production_countries','tagline','released','votes','year','status','score',\
         'popularity'], axis=1, inplace=True)
    df.rename(columns={'original_language': 'language','runtime_x': 'runtime'}, inplace=True)
    # df.rename(columns={'original_language': 'language','runtime_x': 'runtime'}, inplace=True)

#df.set_index('title', inplace=True)
    df.dropna(inplace=True)
    app.run(debug=True)
#df

#     columns_to_drop =['budget', 'genres', 'homepage', 'id','original_language',
#        'overview', 'popularity', 'production_companies',
#        'production_countries', 'release_date', 'revenue', 'runtime',
#        'spoken_languages', 'status', 'tagline','vote_average','vote_count']
#     csv_file = "/home/kevin/Documents/9321/Plan_Z/tmdb_movie/tmdb_5000_movies.csv"
#     df = pd.read_csv(csv_file)
#     df.drop(columns_to_drop, inplace=True, axis=1)
#     df.set_index('original_title', inplace=True)
# #df.loc['Walter Forbes. [A novel.] By A. A']
#     app.run(debug=True)
