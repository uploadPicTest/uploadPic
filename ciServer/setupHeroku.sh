 # The following will add our apt repository and install the CLI:

sudo add-apt-repository "deb https://cli-assets.heroku.com/branches/stable/apt ./"
curl -L https://cli-assets.heroku.com/apt/release.key | sudo apt-key add -
sudo apt-get update
sudo apt-get install heroku

heroku login
cd uploadPic
heroku create
git push heroku master
heroku ps:scale web=1
heroku keys:add $1

NAME=`heroku info -s | grep git_url | cut -d/ -f4`
sed  "s|whispering-meadow-18482.git|$NAME|g" .drone.yml > .drone.yml.temp
cp .drone.yml.temp .drone.yml
git add .drone.yml

cd ..
