from flask import Flask, render_template, request, make_response
from collections import defaultdict
from db import cart_obj, coffee_obj
import datetime

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/menu', methods=['GET', 'POST'])
def menu():
    if request.method == 'POST':
        res = defaultdict(dict)
        [res[int(k.split('-')[1])].update({k.split('-')[0]: float(val)}) for k, val in
         request.form.to_dict().items() if any(k[0] in fl for fl in ['q', 'p']) and float(val) != 0]
        cart_obj.add_to_cart(res)
        if 'Cart' in request.form:
            return render_template('menu.html', items=coffee_obj.get_coffee_ls(), cart_items=cart_obj.get_cart_ls())
        else:
            make_response('GET')
            return cart()
    else:
        return render_template('menu.html', items=coffee_obj.get_coffee_ls(), cart_items=cart_obj.get_cart_ls())


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    details = request.form.to_dict()
    if request.method == 'POST' and details.get('uname', False):
        details = request.form.to_dict()
        return render_check(cart_obj.get_cart_ls(), details)
    else:
        items = cart_obj.get_cart_ls()
        subtotal = round(sum(item[4] for item in items), 2)
        tax_rate = 0.1  # 10% tax
        tax = round(subtotal * tax_rate, 2)
        total = round(subtotal + tax)
        return render_template('cart.html', items=items, subtotal=subtotal, tax=tax, total=total, tax_rate=tax_rate)


@app.route('/check')
def render_check(data, details):
    subtotal = round(sum(item[4] for item in data), 2)
    tax_rate = 0.1  # 10% tax
    tax = round(subtotal * tax_rate, 2)
    total = round(subtotal + tax)
    cart_obj.clear_cart()
    return render_template('check.html', items=data, subtotal=subtotal, tax=tax, total=total,
                           date=datetime.datetime.now(), **details)


@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
