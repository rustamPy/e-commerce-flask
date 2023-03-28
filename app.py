import os
from collections import defaultdict
from database_funcs import add_coffee_to_cart, get_cart_ls, cursor, conn, get_coffee_ls
from flask import Flask, render_template, request


app = Flask(__name__)


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
