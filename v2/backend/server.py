#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#
import os
import time
import zmq

import numpy as np

from sklearn import datasets, svm, metrics
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

def get_model(test_size=0.5, gamma=0.001, shuffle=False):
	digits = datasets.load_digits()
	print(digits.images.shape, digits.images.dtype)
	print(digits.target.shape, digits.target.dtype)

	# flatten the images
	n_samples = len(digits.images)
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
	
	n_train, n_test = len(y_train), len(y_test)

	# Create a classifier: a support vector classifier
	model = svm.SVC(gamma=gamma)

	# Learn the digits on the train subset
	model.fit(X_train, y_train)

	# Predict the value of the digit on the test subset
	predicted = model.predict(X_test)

	print(
		f"Classifier {model} is ready\n"
		#f"{metrics.classification_report(y_test, predicted)}\n"
	)

	return model, meta_dict


def recv_array(socket, flags=0, copy=True, track=False):
	"""recv a numpy array"""
	string = socket.recv_string(flags=flags)
	md = socket.recv_json(flags=flags)
	msg = socket.recv(flags=flags, copy=copy, track=track)
	buf = bytes(memoryview(msg))
	A = np.frombuffer(buf, dtype=md['dtype'])
	return string, A.reshape(md['shape'])

def main():

	model, model_meta = get_model()
	context = zmq.Context()
	socket = context.socket(zmq.REP)
	address = os.environ.get('SERVER_LISTEN_URI')
	socket.bind(address)


	fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(5, 5))
	while True:

		my_str, my_array = recv_array(socket)
		print(f'Server got request: {my_str}')
		img = np.reshape(my_array, model_meta['image_size'])
		ax.imshow(img, cmap=plt.cm.gray_r, interpolation="nearest")
		plt.savefig(f'{my_str}.png')
		
		predicted = model.predict(my_array.reshape(1,-1))
		
		socket.send_unicode(f'pred of {my_str} is: {predicted}')


if __name__ == '__main__':

	main()
