#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#
import os 
import zmq
import numpy as np
import random
from sklearn import datasets, svm, metrics
from sklearn.model_selection import train_test_split

def get_data(test_size=0.5, shuffle=False):
	"""Get test image data 
	
	Args:
		test_size: Split of dataset for test
		shuffle: Set to `True` when shuffling dataset

	Returns:
		X_test: test data after flattening 
	"""
	digits = datasets.load_digits()

	# flatten the images
	n_samples = len(digits.images)
	data = digits.images.reshape((n_samples, -1))
	
	# Split data into 50% train and 50% test subsets
	X_train, X_test, y_train, y_test = train_test_split(
		data, digits.target, test_size=test_size, shuffle=shuffle
	)

	return X_test
	
def send_array(socket, A, string, flags=0, copy=True, track=False):
	"""send a numpy array with metadata"""
	
	md = dict(dtype = str(A.dtype), shape = A.shape,)
	socket.send_string(string, flags|zmq.SNDMORE)
	socket.send_json(md, flags|zmq.SNDMORE)
	return socket.send(A, flags, copy=copy, track=track)

def main():

	k_test = 5 # predict k_test images randomly
	test_data = get_data()
	context = zmq.Context()

	#  Socket to talk to server
	print("Connecting to digit recognition server…")
	socket = context.socket(zmq.REQ)
	address = os.environ.get('SERVER_CONNECT_URI')
	socket.connect(address)

	num_test = test_data.shape[0]
	assert num_test > 0, 'Test data not loaded'
	k = k_test if num_test>k_test else num_test

	test_list = random.sample(range(num_test), k=k)
	for test_id in test_list:
		my_str = f'{test_id}'
		my_array= test_data[test_id]
		print(f'Client sent request: image {my_str}')
		send_array(socket, my_array, my_str)
		rep = socket.recv_unicode()
		print(f'Client got reply: {rep}\n')

if __name__ == '__main__':

	main()