#!/bin/bash

#Set up needed local packages
sudo apt-get update
sudo apt-get install curl
#sudo apt-get install linux-image-extra-$(uname -r) linux-image-extra-virtual

#Prep docker repos - note that automating this is a bit risky
sudo apt-get install apt-transport-https ca-certificates
curl -fsSL https://yum.dockerproject.org/gpg | sudo apt-key add -
sudo add-apt-repository \
       "deb https://apt.dockerproject.org/repo/ \
       ubuntu-$(lsb_release -cs) \
       main"

#Actually install docker
sudo apt-get update
sudo apt-get -y install docker-engine

