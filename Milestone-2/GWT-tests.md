
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
