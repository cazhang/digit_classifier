#
#   Digit Recognition client in Python
#   Connects REQ socket to tcp://0.0.0.0:5555
#   Sends "Image" to server, expects "Prediction" back
#

import zmq
import numpy as np
import random
from sklearn import datasets, svm, metrics
from sklearn.model_selection import train_test_split

def get_data(test_size=0.5, shuffle=False):
	digits = datasets.load_digits()
	print(digits.images.shape, digits.images.dtype)
	print(digits.target.shape, digits.target.dtype)

	# flatten the images
	n_samples = len(digits.images)
	img_size = digits.images.shape[1:3]
	data = digits.images.reshape((n_samples, -1))
	
	# Split data into 50% train and 50% test subsets
	X_train, X_test, y_train, y_test = train_test_split(
		data, digits.target, test_size=test_size, shuffle=shuffle
	)
	
	n_train, n_test = len(y_train), len(y_test)

	print(f'Get test data {X_test.shape}')
	return X_test
	
def send_array(socket, A, string, flags=0, copy=True, track=False):
	"""send a numpy array with metadata"""
	
	md = dict(dtype = str(A.dtype), shape = A.shape,)
	socket.send_string(string, flags|zmq.SNDMORE)
	socket.send_json(md, flags|zmq.SNDMORE)
	return socket.send(A, flags, copy=copy, track=track)

def main():

	data = get_data()
	context = zmq.Context()

	#  Socket to talk to server
	print("Connecting to digit recognition server…")
	socket = context.socket(zmq.REQ)
	socket.connect("tcp://0.0.0.0:5555")

	n_test = data.shape[0]
	assert n_test > 0, 'Test data not loaded'
	k = 5 if n_test>5 else n_test

	test_list = random.sample(range(n_test), k=k)
	for test_id in test_list:
		my_str = f'{test_id}'
		my_array= data[test_id]
		print(f'Client sent request: image {my_str}')
		send_array(socket, my_array, my_str)
		rep = socket.recv_unicode()
		print(f'Client got reply: {rep}')

if __name__ == '__main__':

	main()