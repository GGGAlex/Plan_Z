import pandas as pd
from flask import Flask
from flask_restplus import Api,Resource

app = Flask(__name__)
api = Api(app)

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

if __name__ == '__main__':

    columns_to_drop =['budget', 'genres', 'homepage', 'id','original_language',
       'overview', 'popularity', 'production_companies',
       'production_countries', 'release_date', 'revenue', 'runtime',
       'spoken_languages', 'status', 'tagline','vote_average','vote_count']
    csv_file = "/home/kevin/Documents/9321/Plan_Z/tmdb_movie/tmdb_5000_movies.csv"
    df = pd.read_csv(csv_file)
    df.drop(columns_to_drop, inplace=True, axis=1)
    df.set_index('original_title', inplace=True)
#df.loc['Walter Forbes. [A novel.] By A. A']
    app.run(debug=True)
