# OBS4
Online Banking System

Do 
virtualenv env <br/>
source env/bin/activate <br/> 
pip3 install -r requirements <br/> 
export(Mac) or set(Windows) SECRET_KEY= "Choose a Key here" <br/>
Either set FLASK_APP or python3 main.py <br/>
On a seperate terminal python3 apis/"api name"

# Document  <br/> 
Repo Link: https://github.com/kwaku97/OBS4  <br/> 
Styling Format PeP8: https://www.python.org/dev/peps/pep-0008/  <br/> 
Swagger Hub Documentation: https://github.com/kwaku97/OBS4/blob/master/Milestone-2/openapi.yaml  <br/> 

If a rollback was necessary, git allows you to go back to a specific commit by specifying the commmit tag given at that commit. The command I would reccomend is  git checkout -b old-state #tag. This command will switch to a new branch using the tag of the time frame you want. This will allow you to be on a new bracnh and try it out before actually merging and changing everything. If you are sure from the beginnning, you can use the command git reset --hard #tag. This will reset everything you did up to the tag you specified. 

We used Python as our primary language of choice. With Flask we are serving information to the front end by specfic routes and handling requests on the backend. For this project we used three different databases. The firstt database handles the register and login information about the user. This database uses POSTGRES and with the help of SQLAlchemy, modeling the table was simple.We the retrieved the data using WTForms which is a python library that rpovides login and registration support. For storing information about the users shares,different accounts,cash and net worth we used another POSTGRES database to do the math and hold that information. Finally for our APIs we used firebase. We used firebase to store sucessful/failed purhcases and success/failed login attempts. We used Python's Jwt library to provide a token everytime a user is logged in and it apppears on the front page when login is successful. 

Our Repo Configuration mainly consists of our web client as one seperate entity and our apis/test as its own entity. Through specific request, calls are made to make that conenction. We use Google Cloud Build to create our CD pipeline. Our pipline is connect to our Github repo's master branch. When a new push is made to the remote branch, a build is triggered to create a base docker image that contains our github repo and our environment variables. From this base image we run our unit tests. Then if the tests past we create four stock APIs docker images, and a docker image for our web client. After creating the images we deploy our services to Cloud Run.
