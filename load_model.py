import pickle 
import scipy
import lifelines

def load_model():
	with open("BRCA2_model.pickle", "rb") as input_file:
		model = pickle.load(input_file)
		#print(model.hazards_)
		return model
#model = load_model()