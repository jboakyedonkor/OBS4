import psycopg2

conn = psycopg2.connect(host="127.0.0.1", database="test-instance", user="postgres", password="password", port="3306")


def execute_sql(command):
    cur = conn.cursor()
    cur.execute(command)
    cur.close()
    conn.commit()


def getTimeStamp():
    dateTimeObj = datetime.now()
    return dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")

def create_transaction_table():
    command = """
            CREATE TABLE transaction_logs_table (
                    auto_id SERIAL PRIMARY KEY,
                    tran_timestmp DATE NOT NULL,
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


def create_user_table():
    command = """"
    CREATE TABLE user_table (
     auto_id VARCHAR(40),
     username VARCHAR(40),
     password VARCHAR(40),
     account_name VARCHAR(40),
     account_num INTEGER
    )
    """
    execute_sql(command)


def create_stock_table():
    command = """
    CREATE TABLE stock_table (
     auto_id SERIAL PRIMARY KEY,
     symbol TEXT,
     num_shares INT NOT NULL
    """
    execute_sql(command)


def populate_stock_table():
    command = """"    
    INSERT INTO stock_table VALUES( ('MSFT', '5000') ,('AAPL', '5000') ,('GOOG', '5000') ,('FB', '5000') ,('TWT', '5000'));
    """
    execute_sql(command)


def populate_banking_table():
    command = """"    
    INSERT INTO banking_table VALUES( ('MSFT', '0') ,('AAPL', '0') ,('GOOG', '0') ,('FB', '0') ,('TWT', '0'));
    """
    execute_sql(command)


def update_stock_table(stock_symbol, stock_purchased, buy):
    cursor = conn.cursor()
    remaining_user_stock = "SELECT * " + "FROM stock_table" + "WHERE symbol = " + stock_symbol
    cursor.execute(remaining_user_stock)
    getCurrentUserStock = cursor.fetchone()
    cursor.close()
    conn.commit()

    if (buy == false):
        final_user_stock = getCurrentUserStock - stock_purchased
    else:
        final_user_stock = getCurrentUserStock + stock_purchased

    command = "UPDATE TABLE stock_table SET num_shares = " + final_user_stock + " WHERE symbol = " + stock_symbol
    execute_sql(command)


def update_bank_table(stock_symbol, stock_purchased, buy):
    cursor = conn.cursor()
    remaining_bank_stock = "SELECT * " + "FROM banking_table" + "WHERE symbol = " + stock_symbol
    cursor.execute(remaining_bank_stock)
    getCurrentBankStock = cursor.fetchone()
    cursor.close()
    conn.commit()

    if (buy == true):
        final_bank_stock = getCurrentBankStock - stock_purchased
    else:
        final_bank_stock = getCurrentBankStock + stock_purchased

    command = "UPDATE TABLE banking_table SET num_shares = " + final_bank_stock + " WHERE symbol = " + stock_symbol
    execute_sql(command)


def insert_transaction_logs_table(symbol, ask_price, num_shares, username, account, buy_or_sell, key_used):
    command = "INSERT INTO transaction_logs_table VALUES( " + getTimeStamp() + ", " + symbol + ", " + ask_price + ", "
    num_shares + ", " + username + + ", " + account + ", " + buy_or_sell + ", " + key_used + ")"
    execute_sql(command)


def insert_user_table(username, password, account_name, account_num):
    command = "INSERT INTO user_table VALUES( " + username + ", " + password + ", " + account_name + ", " + account_num + ")"
    execute_sql(command)


def drop_user_table():
    command = """ DROP TABLE user_table """
    execute_sql(command)


def drop_transaction_logs_table():
    command = """ DROP TABLE transaction_logs_table """
    execute_sql(command)
