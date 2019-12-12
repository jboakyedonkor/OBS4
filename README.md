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

For this project we used three different databases. The firstt database handles the register and login information about the user. This database uses POSTGRES and with the help of SQLAlchemy, modeling the table was simple.We the retrieved the data using WTForms which is a python library that rpovides login and registration support. For storing information about the users shares,different accounts,cash and net worth we used another POSTGRES database to do the math and hold that information. Finally for our APIs we used firebase. We used firebase to store sucessful/failed purhcases and success/failed login attempts. We used Python's Jwt library to provide a token everytime a user is logged in and it apppears on the front page when login is successful. 
