import warnings;
import joblib
warnings.simplefilter('ignore')



class recommender():

	def __init__(self):
		self.indices = joblib.load('indices')
		self.smd = joblib.load('smd')
		self.cosine_sim = joblib.load('cosine')

	def improved_recommendations(self,title):
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
		# 贝叶斯统计算法来计算电影得分
		qualified['wr'] = qualified.apply(lambda x:(x['vote_count'] /
		                                            (x['vote_count'] + m) * x['vote_average'])
		                                           + (m / (m + x['vote_count']) * C), axis=1)
		qualified = qualified.sort_values('wr', ascending=False).head(10)
		return qualified




a=recommender()
qu = a.improved_recommendations("Spider-Man 3")
print(qu)