import os
from collections import defaultdict

from flask import Flask, render_template, request
import pyodbc

app = Flask(__name__)
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


@app.route('/menu', methods=['GET', 'POST'])
def menu():
    if request.method == 'POST':
        res = defaultdict(dict)
        for key, val in request.form.to_dict().items():
            if 'quan' in key:
                res[key.split('-')[1]]['quan'] = val
            else:
                res[key.split('-')[1]]['pr'] = val

        [add_coffee_to_cart(k, res[k]['quan'], res[k]['pr']) for k, _ in res.items()]
        cart_items: list = get_cart_ls()
        # clear cart
        cursor.execute("DELETE FROM cart_t")
        conn.commit()

        return render_template('cart_items.html', items=cart_items)
    else:
        return render_template('menu.html', items=get_coffee_ls())


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# about
@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run()
