import psycopg2
from datetime import datetime
import datetime
import time


conn = psycopg2.connect('postgres://bdhcskpn:aN7RtxPZgnKxxjWBhOGzaSi5uVigON4l@salt.db.elephantsql.com:5432/bdhcskpn')

class checkMethods:
    def checkUsername(pass_username):
        cursor = conn.cursor()
        command = "SELECT COUNT(*) FROM user_table WHERE username = '" + pass_username + "'"
        cursor.execute(command)
        getAccNo = cursor.fetchone()
        cursor.close()
        conn.commit()
        if getAccNo >= 1:
            return True
        else:
            return False



    def checkBankTableStock(pass_symbol):
        cursor = conn.cursor()
        command = "SELECT num_shares FROM bank_table WHERE symbol = '" + pass_symbol + "'"
        cursor.execute(command)
        numBankStock = int(cursor.fetchone()[0])
        print(numBankStock)
        cursor.close()
        conn.commit()
        return int(numBankStock)

    def checkClientTableStock(pass_symbol):
        cursor = conn.cursor()
        command = "SELECT num_shares FROM client_table WHERE symbol = '" + pass_symbol + "'"
        cursor.execute(command)
        numClientStock = int(cursor.fetchone()[0])
        cursor.close()
        conn.commit()
        return int(numClientStock)

class insertMethods:

    def insert_transaction_logs_table(symbol, ask_price, num_shares, username, buy_or_sell):
        command = "INSERT INTO  transaction_logs_table (tran_timestmp, symbol, ask_price, num_shares, username,  buy_or_sell) VALUES( now(), '" + symbol + "', '" + str(ask_price) + "', '"+ str(num_shares) + "', '" \
                  + username + "', '" + buy_or_sell +"')"
        execute_sql(command)


    def insert_user_table(username, password, account_name, account_number):
        command = "INSERT INTO user_table (username, password, account_name, account_number) VALUES( '" + username + "', '" + password + "', '" + account_name + "', '" + str(account_number) + "')"
        execute_sql(command)


class updateMethods:
    def update_bank_table(stock_symbol, stock_purchased, buy):
        cursor = conn.cursor()
        remaining_bank_stock = "SELECT * " + "FROM bank_table WHERE symbol = '" + stock_symbol + "'"
        cursor.execute(remaining_bank_stock)
        getCurrentBankStock = int(cursor.fetchone()[2])
        cursor.close()
        conn.commit()
        print(getCurrentBankStock)

        if (buy == True):
            final_bank_stock = getCurrentBankStock - stock_purchased
        else:
            final_bank_stock = getCurrentBankStock + stock_purchased

        command = "UPDATE bank_table SET num_shares = " + str(final_bank_stock) + " WHERE symbol = '" + stock_symbol + "'"
        execute_sql(command)

    def update_client_table(stock_symbol, stock_purchased, buy):
        cursor = conn.cursor()
        remaining_client_stock = "SELECT * " + "FROM client_table WHERE symbol = '" + stock_symbol + "'"
        cursor.execute(remaining_client_stock)
        getCurrentClientStock = int(cursor.fetchone()[2])
        cursor.close()
        conn.commit()

        if (buy == True):
            final_client_stock = getCurrentClientStock + stock_purchased
        else:
            final_client_stock = getCurrentClientStock- stock_purchased

        command = "UPDATE client_table SET num_shares = " + str(
            final_client_stock) + " WHERE symbol = '" + stock_symbol + "'"
        execute_sql(command)

def execute_sql(command):
    cur = conn.cursor()
    cur.execute(command)
    cur.close()
    conn.commit()


def getTimeStamp():
    return datetime.datetime.today()


def create_transaction_table():
    command = """
            CREATE TABLE transaction_logs_table (
                    auto_id SERIAL PRIMARY KEY,
                    tran_timestmp VARCHAR(40) NOT NULL,
                    symbol TEXT NOT NULL,
                    ask_price REAL NOT NULL,
                    num_shares INT NOT NULL,
                    username TEXT NOT NULL,
                    buy_or_sell TEXT NOT NULL
            )
            """
    execute_sql(command)


def create_client_table():
    command = """
    CREATE TABLE client_table(
      auto_id SERIAL PRIMARY KEY,
                    symbol TEXT NOT NULL,
                    num_shares INT NOT NULL           
    )
    """
    execute_sql(command)


def create_user_table():
    command = """
    CREATE TABLE user_table (
     auto_id SERIAL PRIMARY KEY,
     username TEXT NOT NULL,
     password TEXT NOT NULL,
     account_name TEXT NOT NULL,
     account_number INT
    )
    """
    execute_sql(command)


def create_bank_table():
    command = """
    CREATE TABLE bank_table (
     auto_id SERIAL PRIMARY KEY,
     symbol TEXT,
     num_shares INT NOT NULL
     )
    """
    execute_sql(command)


def populate_bank_table():
    command = "INSERT INTO bank_table (symbol, num_shares) VALUES ('MSFT', '5000');"
    execute_sql(command)
    command = "INSERT INTO bank_table (symbol, num_shares) VALUES ('AAPL', '5000');"
    execute_sql(command)
    command = "INSERT INTO bank_table (symbol, num_shares) VALUES ('GOOG', '5000');"
    execute_sql(command)
    command = "INSERT INTO bank_table (symbol, num_shares) VALUES ('FB', '5000');"
    execute_sql(command)


def populate_client_table():
    command = "INSERT INTO client_table (symbol, num_shares) VALUES ('MSFT', '0');"
    execute_sql(command)
    command = "INSERT INTO client_table (symbol, num_shares) VALUES ('AAPL', '0');"
    execute_sql(command)
    command = "INSERT INTO client_table (symbol, num_shares) VALUES ('GOOG', '0');"
    execute_sql(command)
    command = "INSERT INTO client_table (symbol, num_shares) VALUES ('FB', '0');"
    execute_sql(command)


def drop_user_table():
    command = """ DROP TABLE user_table """
    execute_sql(command)

def drop_transaction_logs_table():
    command = """ DROP TABLE transaction_logs_table """
    execute_sql(command)
#create_transaction_table()
def drop_bank_table():
    command = """ DROP TABLE bank_table """
    execute_sql(command)

def drop_client_table():
    command = """ DROP TABLE client_table """
    execute_sql(command)


def startOver():
    drop_client_table()
    drop_transaction_logs_table()
    drop_bank_table()
    time.sleep(0.5)
    create_bank_table()
    create_transaction_table()
    create_client_table()
    time.sleep(0.3)
    populate_client_table()
    populate_bank_table()
