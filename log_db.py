import psycopg2
from datetime import datetime
import datetime

conn = psycopg2.connect(host="127.0.0.1", database="test-instance", user="postgres", password="password", port="3306")


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
                    account TEXT NOT NULL,
                    buy_or_sell TEXT NOT NULL,
                    key_used TEXT NOT NULL
            )
            """
    execute_sql(command)


def create_banking_table():
    command = """
    CREATE TABLE banking_table(
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


def create_stock_table():
    command = """
    CREATE TABLE stock_table (
     auto_id SERIAL PRIMARY KEY,
     symbol TEXT,
     num_shares INT NOT NULL
     )
    """
    execute_sql(command)


def populate_stock_table():
    command = "INSERT INTO stock_table (symbol, num_shares) VALUES ('MSFT', '5000');"
    execute_sql(command)
    command = "INSERT INTO stock_table (symbol, num_shares) VALUES ('AAPL', '5000');"
    execute_sql(command)
    command = "INSERT INTO stock_table (symbol, num_shares) VALUES ('GOOG', '5000');"
    execute_sql(command)
    command = "INSERT INTO stock_table (symbol, num_shares) VALUES ('FB', '5000');"
    execute_sql(command)
    command = "INSERT INTO stock_table (symbol, num_shares) VALUES ('TWT', '5000');"
    execute_sql(command)


def populate_banking_table():

    command = "INSERT INTO banking_table (symbol, num_shares) VALUES ('MSFT', '0');"
    execute_sql(command)
    command = "INSERT INTO banking_table (symbol, num_shares) VALUES ('AAPL', '0');"
    execute_sql(command)
    command = "INSERT INTO banking_table (symbol, num_shares) VALUES ('GOOG', '0');"
    execute_sql(command)
    command = "INSERT INTO banking_table (symbol, num_shares) VALUES ('FB', '0');"
    execute_sql(command)
    command = "INSERT INTO banking_table (symbol, num_shares) VALUES ('TWT', '0');"
    execute_sql(command)


def update_stock_table(stock_symbol, stock_purchased, buy):
    cursor = conn.cursor()
    remaining_user_stock = "SELECT * " + "FROM stock_table WHERE symbol = '" + stock_symbol + "'"
    cursor.execute(remaining_user_stock)
    getCurrentUserStock = cursor.fetchone()
    cursor.close()
    conn.commit()

    if (buy == False):
        final_user_stock = getCurrentUserStock[2] - stock_purchased
    else:
        final_user_stock = getCurrentUserStock[2] + stock_purchased

    command = "UPDATE stock_table SET num_shares = " + str(final_user_stock) + " WHERE symbol = '" + stock_symbol + "'"
    execute_sql(command)


def update_bank_table(stock_symbol, stock_purchased, buy):
    cursor = conn.cursor()
    remaining_bank_stock = "SELECT * " + "FROM banking_table WHERE symbol = '" + stock_symbol +"'"
    cursor.execute(remaining_bank_stock)
    getCurrentBankStock = cursor.fetchone()
    cursor.close()
    conn.commit()

    if (buy == True):
        final_bank_stock = getCurrentBankStock[2] - stock_purchased
    else:
        final_bank_stock = getCurrentBankStock[2] + stock_purchased

    command = "UPDATE banking_table SET num_shares = " + str(final_bank_stock) + " WHERE symbol = '" + stock_symbol + "'"
    execute_sql(command)


def insert_transaction_logs_table(symbol, ask_price, num_shares, username, account, buy_or_sell, key_used):
    command = "INSERT INTO  transaction_logs_table (tran_timestmp, symbol, ask_price, num_shares, username, account, buy_or_sell, key_used) VALUES( now(), '" + symbol + "', '" + str(ask_price) + "', '"+ str(num_shares) + "', '" \
              + username + "', '" + account + "', '" + buy_or_sell + "', '" + key_used + "')"
    execute_sql(command)


def insert_user_table(username, password, account_name, account_number):
    command = "INSERT INTO user_table (username, password, account_name, account_number) VALUES( '" + username + "', '" + password + "', '" + account_name + "', '" + str(account_number) + "')"
    execute_sql(command)


def drop_user_table():
    command = """ DROP TABLE user_table """
    execute_sql(command)


def drop_transaction_logs_table():
    command = """ DROP TABLE transaction_logs_table """
    execute_sql(command)


#update_stock_table('MSFT', 500, False)
#drop_transaction_logs_table()
#create_transaction_table()
#insert_transaction_logs_table('MSFT', 23.00, 25, 'yeeeet', 'yeet1', 'Buy', 'EONFGR2343er')
#drop_user_table()
#create_user_table()

# def getAccNo(username):
# 
#     cursor = conn.cursor()
#     command = "SELECT COUNT(*) FROM user_table WHERE username = '" + username + "'"
# 
#     cursor.execute(command)
#     getAccNo = cursor.fetchone()
#     cursor.close()
#     conn.commit()
# 
#     return getAccNo[0] + 1

