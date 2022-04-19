# Server/Client Digit Image Classification with Docker support

## Features
- python zmq-based server/client implementation 
- docker support with docker-compose
- Dockerfile in `frontend` and `backend` include details of client and server
- `docker-compose.yml` shows how to build two services together

## How To Use
- in the folder, command `docker-compose up` to build and run the application
- server received client requests (5 random images) and sent back predictions
- command `docker run -v v2_myvol2:/v2_myvol2 -it ubuntu` to access processed images 
- command `docker-compose down --volumes` to close

