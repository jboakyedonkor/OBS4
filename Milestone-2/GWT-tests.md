
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
