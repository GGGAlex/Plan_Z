# get, delete, put 
import pandas as pd
from flask import Flask
from flask import request
from flask_restplus import Resource, Api
from flask_restplus import fields

app = Flask(__name__)
api = Api(app)

# The following is the schema of Mushrooms
# ##################################################################################### Need to be modified
mushrooms_model = api.model('Mushrooms', {
    # 'Flickr_URL': fields.String,
    # 'Publisher': fields.String,
    # 'Author': fields.String,
    # 'Title': fields.String,
    # 'Date_of_Publication': fields.Integer,
    # 'Identifier': fields.Integer,
    # 'Place_of_Publication': fields.String
})
# ##################################################################################### End 

@api.route('/mushroom/data/<feature_class>')
class Mushrooms(Resource):
    def get(self, feature_class):
        if feature_class not in df.columns:
            api.abort(404, "{} doesn't exist".format(feature_class))
        else:
        	df1 = df.loc[:, ['class', feature_class]]
        	df2 = df1.loc[df1[feature_class] == feature]
        	total = len(df2)
        	df2 = df2.groupby('class').count()
        	e_number = df2.loc['e', feature_class]
        return round(e_number * 100 / total, 2)

    # def delete(self, id):
    #     if id not in df.index:
    #         api.abort(404, "Book {} doesn't exist".format(id))

    #     df.drop(id, inplace=True)
    #     return {"message": "Book {} is removed.".format(id)}, 200

    # @api.expect(book_model)
    # def put(self, id):

    #     if id not in df.index:
    #         api.abort(404, "Book {} doesn't exist".format(id))

    #     # get the payload and convert it to a JSON
    #     book = request.json

    #     # Book ID cannot be changed
    #     if 'Identifier' in book and id != book['Identifier']:
    #         return {"message": "Identifier cannot be changed".format(id)}, 400

    #     # Update the values
    #     for key in book:
    #         if key not in book_model.keys():
    #             # unexpected column
    #             return {"message": "Property {} is invalid".format(key)}, 400
    #         df.loc[id, key] = book[key]

    #     # df.append(book, ignore_index=True)
    #     return {"message": "Book {} has been successfully updated".format(id)}, 200


if __name__ == '__main__':
    # columns_to_drop = ['Edition Statement',
    #                    'Corporate Author',
    #                    'Corporate Contributors',
    #                    'Former owner',
    #                    'Engraver',
    #                    'Contributors',
    #                    'Issuance type',
    #                    'Shelfmarks'
    #                    ]
    csv_file = "mushrooms.csv"
    df = pd.read_csv(csv_file)

    # drop unnecessary columns
    # df.drop(columns_to_drop, inplace=True, axis=1)

    # clean the date of publication & convert it to numeric data
    # new_date = df['Date of Publication'].str.extract(r'^(\d{4})', expand=False)
    # new_date = pd.to_numeric(new_date)
    # new_date = new_date.fillna(0)
    # df['Date of Publication'] = new_date

    # replace spaces in the name of columns
    # df.columns = [c.replace(' ', '_') for c in df.columns]

    # set the index column; this will help us to find books with their ids
    # df.set_index('Identifier', inplace=True)

    # run the application
    app.run(debug=True)
