#/bin/bash

#This sets up drone, assuming docker is installed
mkdir droneio
sed 's|<CLIENT_TOKEN_HERE>|$1|' uploadPic/ciServer/Dockerfile > droneio/tempfile
sed 's|<CLIENT_SECRET_HERE>|$2|' droneio/tempfile > droneio/Dockerfile
touch droneio/drone.sqlite

#Next, build the Docker image
cd droneio
docker build -t my_drone .


docker run -d --name="drone-ci"     -p 8080:8080     -v /var/lib/drone/     -v /var/run/docker.sock:/var/run/docker.sock     -v $PWD/droneio/drone.sqlite:/var/lib/drone/drone.sqlite     my_drone
78903eb22a51d56bde8d552c50d02a1abc109028c225fd0b6289db1e354e3c0e

cd ..

