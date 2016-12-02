import os
import extract_features
import extract_goldlabel
from sklearn import linear_model
from sklearn import metrics 
import pickle

class Classifier:

	def __init__(self):
            
            self.DATA_PATH = '\DataSet\Timeline17\Data'
            self.METADATA_PATH = '\DataSet\Timeline17\MetaData'
            
            self.topic_list = ['bpoil_bbc','bpoil_foxnews','bpoil_guardian','bpoil_reuters','bpoil_washingtonpost','EgyptianProtest_cnn','Finan_washingtonpost','H1N1_bbc','H1N1_guardian','H1N1_reuters','haiti_bbc','IraqWar_guardian','LibyaWar_cnn','LibyaWar_reuters','MJ_bbc','SyrianCrisis_bbc','SyrianCrisis_reuters']
            self.date_list = []
            self.gold_label = []
            self.featurevector_list = []

            self.clf = linear_model.LogisticRegression()
            

	def create_metadata(self):

		root_path = os.path.join(self.DATA_PATH)
		metadata_path = os.path.join(self.METADATA_PATH)
		feat = extract_features.Features()
		output_var = extract_goldlabel.GoldLabel()
		
		for directory in self.topic_list:
		
				print "Getting feature vector for ", directory
				date_list, featurevector_list = feat.create_featurevector(directory)

				print "Getting gold labels for ", directory
				gold_label = output_var.get_goldlabel(directory, date_list)

				output = open( directory+'date_list.txt', 'wb')
				pickle.dump(date_list, output)
				output.close()
				
				output = open( directory+'featurevector_list.txt', 'wb')
				pickle.dump(featurevector_list, output)
				output.close()
				
				output = open( directory+'gold_label.txt', 'wb')
				pickle.dump(gold_label, output)
				output.close()
				
		pass

	def get_data(self):

		root_path = os.path.join(self.METADATA_PATH)
		feat = extract_features.Features()
		output = extract_goldlabel.GoldLabel()
		
		for directory in self.topic_list:

			input1 = open(directory+'date_list.txt', 'rb')
			date_list = pickle.load(input1)
			input1.close()

			input1 = open(directory+'featurevector_list.txt', 'rb')
			featurevector_list = pickle.load(input1)
			input1.close()

			input1 = open(directory+'gold_label.txt', 'rb')
			gold_label = pickle.load(input1)
			input1.close()

			if directory != 'SyrianCrisis_reuters':
					print "Training on ", directory
					self.train_classifier(featurevector_list, gold_label, date_list)
			else:
					self.featurevector_list = featurevector_list
					self.date_list = date_list
					self.gold_label = gold_label

	def train_classifier(self, featurevector_list, gold_label, date_list):

		self.clf.fit(featurevector_list, gold_label)

		pass

	def test_classifier(self):

		ypred = self.clf.predict(self.featurevector_list)
		print "Accuracy Score", metrics.accuracy_score(self.gold_label, ypred)
	
		pass