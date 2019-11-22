import joblib

class classifier():
	def __init__(self):
		self.model=joblib.load('model.m')

	def predict(self,data):
		#data cap-shape cap-surface cap-color odor
		list=['cap-shape_b', 'cap-shape_c', 'cap-shape_f', 'cap-shape_k', 'cap-shape_s', 'cap-shape_x', 'cap-surface_f',
		 'cap-surface_g', 'cap-surface_s', 'cap-surface_y', 'cap-color_b', 'cap-color_c', 'cap-color_e', 'cap-color_g',
		 'cap-color_n', 'cap-color_p', 'cap-color_r', 'cap-color_u', 'cap-color_w', 'cap-color_y', 'odor_a', 'odor_c',
		 'odor_f', 'odor_l', 'odor_m', 'odor_n', 'odor_p', 'odor_s', 'odor_y']
		features=dict(zip(list, [0 for i in range(len(list))]))
		for k,v in data.items():
			features[k+'_'+v]=1
		features=[v for v in features.values()]
		print(features)
		pre=self.model.predict([features])
		print(pre)
a=classifier()
data={'cap-shape':'x','cap-surface':'s','cap-color':'y','odor':'a'}

a.predict(data)