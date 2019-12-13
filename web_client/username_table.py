import psycopg2
import math
import decimal
conn = psycopg2.connect("postgres://kltrpniy:NkxN5nNSePdu6WIDt-UhStBqTomk7l88@rajje.db.elephantsql.com:5432/kltrpniy") 

def execute_sql(command):
    cur = conn.cursor()
    try:
        cur.execute(command)
    except Exception as e:
        conn.rollback()
    else:
        conn.commit()

    cur.close()


# put this after the user registers
def create_user_table():
    command = """
    CREATE TABLE user_table (
     username VARCHAR(40), 
     account_name VARCHAR(40),
     cash VARCHAR(40),
     signIn VARCHAR(40),
     googl VARCHAR(40),
     aapl VARCHAR(40),
     fb VARCHAR(40),
     msft VARCHAR(40)
    )
    """
    execute_sql(command)


def getUserAccounts(username):
    command = "SELECT account_name FROM user_table WHERE username = \'" + username + "\'"

    print(command)
    execute_sql(command)
    print(command)

    cur = conn.cursor()
    cur.execute(command)
    getAccNames = cur.fetchall()
    userAccs = []

    for row in getAccNames:
        userAccs.append(row[0])
        print(row[0])
    cur.close()
    conn.commit()

    return userAccs


def insert_user_table(username, account_name, cash, signIn, googl, aapl, fb, msft):
    command = "INSERT INTO user_table(username, account_name, cash, signIn, googl, aapl, fb, msft) " \
              "VALUES(" + "\'" + username + "\', \'" + account_name + "\', \'" \
              + cash + "\', \'" + signIn + "\', \'" + googl + "\', \'" + aapl + "\', \'" + fb + "\', \'" + msft + "\')"
    print(command)
    execute_sql(command)


def updateSignIn(sign, username, account):
    command = "UPDATE user_table SET signIn = \'" + sign + "\' " \
              + " WHERE account_name = \'" + account + "\' AND  username = \'" + username + "\'"
    execute_sql(command)
    print(command)


def insertFunds(username, account_name, pass_cash):
    prevCash = float(getPrevFunds(username, account_name))
    prevCash = prevCash + float(pass_cash)
    print(prevCash)
    cash = float(prevCash)
    print("insertfundshere")
    print(cash)
    print(str(round(cash, 2)))
    command = "UPDATE user_table SET cash = \'" + str(round(cash, 2)) + "\' " + " WHERE account_name = \'" + \
              account_name + "\' AND  username = \'" + username + "\'"

    print(command)
    execute_sql(command)


def insertBuyFunds(username, account_name, pass_cash):
    prevCash = float(getPrevFunds(username, account_name))
    prevCash = prevCash + float(pass_cash)
    cash = str(prevCash)
    command = "UPDATE user_table SET cash = \'" + cash + "\' " + " WHERE account_name = \'" + \
              account_name + "\' AND  username = \'" + username + "\'"
    print(command)
    execute_sql(command)


def getPrevFunds(username, account_name):
    command = "SELECT cash FROM user_table " + " WHERE account_name = \'" + account_name + "\' AND  username = \'" + username + "\'"
    execute_sql(command)

    cur = conn.cursor()
    cur.execute(command)
    prevFund = cur.fetchall()
    cur.close()
    conn.commit()
    tempFund = (str(prevFund[0])[2:-3])
    finalFund = round(float(tempFund), 2)

    return finalFund


def getShareNum(username, account_name, symbol):
    command = "SELECT " + symbol + " FROM user_table " + " WHERE account_name = \'" + account_name + "\' AND  username = \'" + username + "\'"
    execute_sql(command)

    cur = conn.cursor()
    cur.execute(command)
    shareNum = cur.fetchall()
    cur.close()
    conn.commit()

    return float(str((shareNum[0]))[2:-3])


def getUserShare(username, symbol):

    command = "SELECT SUM (CAST(" + symbol + " AS FLOAT)) as tot  FROM user_table WHERE username = \'" + username + "\'"
    execute_sql(command)

    cur = conn.cursor()
    cur.execute(command)
    shareNum = cur.fetchall()
    cur.close()
    conn.commit()

    return float(str((shareNum))[2:-3])

def getUserFund(username):

    command = "SELECT SUM (CAST(cash AS FLOAT)) as tot_cash  FROM user_table WHERE username = \'" + username + "\'"
    execute_sql(command)

    cur = conn.cursor()
    cur.execute(command)
    shareNum = cur.fetchall()
    cur.close()
    conn.commit()

    return float(str((shareNum))[2:-3])

def getUserNetworth(username, aapl_price, fb_price, msft_price, goog_price):
    aapl_tot_worth = getUserShare(username, "aapl") * aapl_price
    goog_tot_worth = getUserShare(username, "googl") * goog_price
    msft_tot_worth = getUserShare(username,  "msft") * msft_price
    fb_tot_worth = getUserShare(username, "fb") * fb_price

    return aapl_tot_worth + goog_tot_worth + msft_tot_worth + fb_tot_worth + getUserFund(username)

def updateShares(username, account_name, symbol, buyBool, shares, total_cost):
    # buyBool
    # if true, add previous amount to shares
    # if false, subtract previous amount from shares

    if buyBool:
        prevShares = getShareNum(username, account_name, symbol) + float(shares)

        finalCash = float(getPrevFunds(username, account_name)) - float(total_cost)

    else:
        prevShares = getShareNum(username, account_name, symbol) - float(shares)

        finalCash = float(getPrevFunds(username, account_name)) + float(total_cost)

    command = "UPDATE user_table SET " + symbol + " = \'" + str(prevShares) + "\' , cash = \'" + str(finalCash) + \
              "\' WHERE account_name = \'" + account_name + "\' AND  username = \'" + username + "\'"
    execute_sql(command)


def getAccUser(sign):
    command = "SELECT account_name FROM user_table WHERE signIn = \'" + sign + "\'"
    execute_sql(command)
    print(command)

    cur = conn.cursor()
    cur.execute(command)
    signAcc = cur.fetchall()
    cur.close()
    conn.commit()

    return str(signAcc[0])[2:-3]


def signOutUsers():
    command = "UPDATE user_table SET signIn = \'N\'"
    execute_sql(command)


def accNum(username):
    command = "SELECT COUNT(*) FROM user_table WHERE username = \'" + username + "\'"
    execute_sql(command)

    cur = conn.cursor()
    cur.execute(command)
    accCount = cur.fetchone()
    accCount = accCount[0]
    cur.close()
    conn.commit()

    return int(accCount)


def getCashAcc(account, username):
    command = "SELECT cash FROM user_table WHERE account = \'" + account \
              + "\' AND  username = \'" + username + "\'" + "\') "

    print(command)
    execute_sql(command)

    cur = conn.cursor()
    cur.execute(command)
    cashCount = cur.fetchone()
    cashCount = cashCount[0]
    cur.close()
    conn.commit()
    return int(cashCount)


def drop_user_table():
    command = """ DROP TABLE user_table """
    execute_sql(command)
create_user_table()