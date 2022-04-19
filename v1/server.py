#
#   Digit Recognition server in Python
#   Binds REP socket to tcp://*:5555
#   Expects "Image" from client, replies with "Prediction \in [0-9]"
#

import time
import zmq
import numpy as np

from sklearn import datasets, svm, metrics
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

def get_model(test_size=0.5, gamma=0.001, shuffle=False, eval=False):
	"""get svm model from sklearn, trained on load_digits data

	Args: 
		test_size: Split of dataset for test
		gamma: Kernel coefficient
		shuffle: Set to `True` when shuffling dataset
		eval: Set to `True` when evaluating model

	Returns:
		model: trained classifier
		meta_dict: dictionary of model/dataset parameters

	"""
	digits = datasets.load_digits()

	# flatten the images
	n_samples = len(digits.images)
	assert np.ndim(digits.images)==3, 'Only accept gray-scale images!'
	image_size = digits.images.shape[1:3]
	
	meta_dict={}
	meta_dict['image_size'] = image_size
	meta_dict['test_size'] = test_size
	meta_dict['gamma'] = gamma
	meta_dict['shuffle'] = shuffle
	meta_dict['model_type'] = 'SVM'

	data = digits.images.reshape((n_samples, -1))
	
	# Split data into 50% train and 50% test subsets
	X_train, X_test, y_train, y_test = train_test_split(
		data, digits.target, test_size=test_size, shuffle=shuffle
	)
	# Create a classifier: a support vector classifier
	model = svm.SVC(gamma=gamma)
	# Learn the digits on the train subset
	model.fit(X_train, y_train)
	
	print(f"Classifier server is running... \n")
	print(f'Model Description: {model}')

	if eval:
		# Predict the value of the digit on the test subset
		predicted = model.predict(X_test)
		f"{metrics.classification_report(y_test, predicted)}\n"

	return model, meta_dict


def recv_array(socket, flags=0, copy=True, track=False):
	"""recv a numpy array
	
	Returns:
		string: image index 
		img: image data
	"""
	string = socket.recv_string(flags=flags)
	md = socket.recv_json(flags=flags)
	msg = socket.recv(flags=flags, copy=copy, track=track)
	buf = bytes(memoryview(msg))
	img = np.frombuffer(buf, dtype=md['dtype'])
	return string, img.reshape(md['shape'])

def main():

	model, model_meta = get_model()
	context = zmq.Context()
	socket = context.socket(zmq.REP)
	socket.bind("tcp://*:5555")

	fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(5, 5))

	while True:
		img_str, img_vec = recv_array(socket)
		print(f'Server got request: {img_str}')
		img_array = np.reshape(img_vec, model_meta['image_size'])
		ax.imshow(img_array, cmap=plt.cm.gray_r, interpolation="nearest")
		plt.savefig(f'{img_str}.png')
		print(f'Image saved ==> {img_str}.png \n')
		predicted = model.predict(img_vec.reshape(1,-1))
		socket.send_unicode(f'Prediction of {img_str} ==> {predicted[0]}')

if __name__ == '__main__':

	main()
