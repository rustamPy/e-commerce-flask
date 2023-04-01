from flask import Flask, render_template, request
from collections import defaultdict
from db import cart_obj, coffee_obj

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
            return render_template('cart.html', items=cart_obj.get_cart_ls())
    else:
        return render_template('menu.html', items=coffee_obj.get_coffee_ls())


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if request.method == 'POST':
        [coffee_obj.remove_value_from_db(i[3], i[0]) for i in cart_obj.get_cart_ls()]
        cart_obj.clear_cart()
        return render_template('done.html')
    else:
        return render_template('cart.html', items=cart_obj.get_cart_ls())


@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
