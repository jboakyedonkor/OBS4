Scenario: A new user name Carl wants to open a new account on OBS
Given: Carl has not had an OBS account previously
When: Carl clicks on the Sign Up page AND enters correct password and username.
Then: Carl receives a confirmation AND Auth token AND is redirected to the OBS account page

Scenario: Janice is an OBS client who wants to login access her account information
Given: Janice a current OBS client with valid credentials.
When: Janice clicks on the login page AND enters her username and  password
Then: Janice is taken to the OBS dashboard where she can see all her account information

Scenario : Alex is OBS client who wants to access his OBS dashboard
Given: Alex has not logged into the system AND has URL to his OBS dashboard
When: Alex pastes the URL in his browser
Then:  Alex should be redirected to the login page. 

Scenario: Client Johnny wishes to view current stock prices for Bank Inc stock, and see his client portfolio information
Given: Johnny already has created an account with OBS AND has filled out his portfolio information during registration
When: Johnny opens the “Dashboard” page upon successful login
Then: Johnny can successfully view his respective client portfolio information AND view their current stock prices for Bank Inc stocks

Scenario: Jimmy wishes to login to his OBS to view his stocks, so he must login with his username/password, however he uses an incorrect username/password combination
Given: Jimmy believes he has previously made an OBS account AND uses an incorrect username and password combination to login
When: Jimmy attempts to login using his previously mentioned username and password using an incorrect combination AND receives an error upon using the incorrect combination
Then: Jimmy is unable to successfully login AND view his personal account information AND must successfully input a valid username/password combination that is already registered in the OBS in order to successfully login.

Scenario: Jeremy wants to purchase stocks that are valued greater than his current cash held in his account
Given: Jeremy is currently logged into the OBS system as an authenticated user AND has access to purchase stocks AND can decide how many stocks he would like to purchase at a given price
When: Jeremy attempts to purchase stocks that are valued greater than the cash held in his account AND he is unable to fulfill the transaction AND receives an error relating to insufficient funds
Then: Jeremy is unable to purchase stocks that are valued greater than the cash he currently has in his account

Scenario: Authenticated users can purchase shares and sell existing shares.
Given: The authenticated user has OBS access AND has at least one assets account that owns shares AND has enough funds to buy assets.
When: The user accesses one of their assets accounts in the web browser AND opens the “Manage shares” page in a web browser AND has an authentication token.
Then: The user will be able to select any of the four available assets AND be able to buy more assets AND be able to sell assets AND view the prices for each asset AND be able to view how many of each asset that the user owns AND receive an error notification on the page when the user doesn’t have enough funds to purchase the selected amount of assets.

Scenario: Authenticated users can not be permitted to open more than 3 accounts.
Given: The authenticated user has OBS access AND has no more than 3 assets accounts.
When: The authenticated user attempts to create a new assets account on their personal “Dashboard” page by clicking on the “Add Account” button AND redirected to a “New Account” page.
Then: The user will receive an error message saying that they have reached the maximum number of assets account for that user AND be redirected back to the “Dashboard” when they click on the “Return to Dashboard” button that is the only option available on the page.


Scenario: Joe wants to diversify his portfolio in an organized way and want to create another account
Given: Joe has not previously registered for three accounts AND uses the same email
When: Joe opens the “Registration” page in a web browser AND properly enters the required registration fields (should list what they are and any requirements e.g., 8 character password) 
Then: Bob sees a registration confirmation AND is logged in to the system (i.e., token provided) AND transferred to the OBS dashboard  

Scenario: A user Sam wants to add funds to an account
Given: Sam has previously registered for an account(s) AND signed in using his email and password
When: Sam signs in and gets redirects to the home page showing a token 
Then: Sam can specify which account of the three that he wants to use to adds funds.

Scenario: A user Joe has created multiple accounts and wants to view stock and cash earnings for each sub account. 
Given: Joe has previously registered for an account(s) AND signed in using his email and password
When: Joe signs in and gets redirects to the home page showing a token AND Joe can specify which account of the three that he wants to use to make a transaction.
Then: Joe selects the account he wanted to use AND places the token given to view shares AND purchase shares AND that’s stored in OBS database based on the username Joe selected
