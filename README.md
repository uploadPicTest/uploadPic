# uploadPic

A very simple Flask web app to show you the picture you upload to it.

## Purpose

This small app is basically a test of setting up a CI system using
drone.io, Flask, and Heroku.  The drone system is deployed on a
DigitalOcean box, set to use Ubuntu.

## Setting up Drone

First, the Ubuntu version doesn't have Docker, which we will need.
Adding it is very straightforward, we simply have to add it through
apt-get.  Once logged in to the DO instance, we'll grab the scripts
from this repo to use, either by hand or with

```
git clone https://github.com/RichardOtt/uploadPic.git
```

The scripts live in `uploadPic/ciServer`

To install Docker, just run

```
bash uploadPic/uploadPic/setupDocker.sh
```

This will take a little while and pull things from the repos.  To
allow Drone to integrate with Github, we'll need to authorize Drone.
If our DO instance has IP `138.197.10.170` (substitute your own as
appropriate), log in to Github, go to Settings in the drop-down, then
on the right go to "Authorized Applications".  Then at the bottom
click on "OAuth Applications".  We'll need to create a new one
("Register a new application" in the upper right).  Fill in the fields
as follows:

- Name: pick a name
- Homepage URL: https://138.197.10.170:8080/
- Application description: optional, put anything you'd like
- Authorization callback URL: http://138.197.10.170:8080/api/auth/github.com

Once that's done, we'll get back a `Client ID` and a `Client Secret`,
which we'll need to set up Drone.  They'll be hex values.  Once you have those,
just run

```
bash uploadPic/uploadPic/setupDrone.sh <Client_ID> <Client_Secret>
```

Verify that it's working with

```
docker ps
```

You should see values for the different columns (status, etc).  Only
seeing the column headers indicates failure.  Assuming it worked,
Drone is now up and running!

Now go to the Drone page on a browser `https://138.197.10.170:8080/`, and log
in to your github account.  You'll be asked to authorize and sync, go ahead and
do that.  Then activate your fork of this repo.

