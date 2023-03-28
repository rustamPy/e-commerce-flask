import pyodbc

conn_str = "DRIVER={SQL Server}; SERVER=forkoffee.database.windows.net; DATABASE=mydb;UID=drmohm@forkoffee; PWD=Ferum@1313"
conn = pyodbc.connect(conn_str)

cursor = conn.cursor()


def get_coffee_ls() -> list:
    ls = cursor.execute('select * from coffee_t;')
    return [c for c in ls]


def get_cart_ls() -> list:
    command = """
    SELECT cart_t.quantity, coffee_t.name, cart_t.amount
    FROM cart_t
    JOIN coffee_t ON cart_t.coffee_id = coffee_t.id;
    """
    ls = cursor.execute(command)
    return [i for i in ls]


def add_coffee_to_cart(name, q, a):
    command = """
    INSERT INTO cart_t (coffee_id, quantity, amount) VALUES (?, ?, ?)
    """
    cursor.execute(command, name, q, a)
    conn.commit()
