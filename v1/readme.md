# Separate Server/Client Digit Image Classification

## Features
- zmq is used to communicate bewtween server and client
- `sklearn.datasets.load_digits` is used as the dataset
- `sklearn.svm` is used as the classifier
- client sends the `image index` and `image data`
- server replies the `prediction` and saves images 

## How To Use
- assuming you are in Python 3.7 env (eg. created with Anaconda)
- install dependency: `pip install -r requirements.txt` 
- start server in one shell: `python server.py`
- start client in another shell: `python client.py`
- you should see query images saved locally and results displayed 

