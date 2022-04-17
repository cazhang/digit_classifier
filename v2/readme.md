Steps to simulate server/client digit image classification:

No Docker Support:
1. docker build . --tag digit-classifier
2. docker run -it digit-classifier

With Docker Support:
1. docker-compose up
2. docker-compose down --volumes

Access Data
1. docker run -v docker_proj3_myvol2:/docker_proj3_myvol2 -it ubuntu