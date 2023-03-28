import os
from collections import defaultdict
from database_funcs import add_coffee_to_cart, get_cart_ls, cursor, conn, get_coffee_ls
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# about
@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run()
