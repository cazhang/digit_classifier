Separate Server/Client Digit Image Classification:
- assuming you are in Python 3.7 env (eg. created with Anaconda)
- install dependency with: pip install -r requirements.txt 
- start server in one shell: python server.py
- start client in another shell: python client.py
- you should see query images saved locally and results displayed 

1. docker build . --tag digit-classifier
2. docker run -it digit-classifier
