import urllib.parse

from flask import Flask, render_template, request
from collections import defaultdict
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

params = urllib.parse.quote_plus(
    "Driver={SQL Server};Server=forkoffee.database.windows.net;Database=mydb;Uid=drmohm@forkoffee;Pwd=Ferum@1313;")
conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)

app.config['SECRET_KEY'] = 'supersecret'
app.config['SQLALCHEMY_DATABASE_URI'] = conn_str

# extensions

db = SQLAlchemy(app)
with app.app_context():
    class Coffee(db.Model):
        __tablename__ = 'coffee_t'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(50))
        quantity = db.Column(db.Integer)
        rank = db.Column(db.Integer)
        price = db.Column(db.Float)


    class GetCoffee:
        def get_coffee_ls(self):
            coffee_ls = Coffee.query.all()
            return [(i.id, i.name, i.quantity, i.rank, i.price) for i in coffee_ls]

        def get_coffee_name_by_id(self, id):
            cn = Coffee.query.filter_by(id=id).first()
            return cn.name


    coffee_obj = GetCoffee()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/menu', methods=['GET', 'POST'])
def menu():
    if request.method == 'POST':

        res = defaultdict(dict)
        [res[coffee_obj.get_coffee_name_by_id(int(k.split('-')[1]))].update({k.split('-')[0]: float(val)}) for k, val in
         request.form.to_dict().items() if float(val) != 0]
        return render_template('cart_items.html', items=res)

    else:
        return render_template('menu.html', items=coffee_obj.get_coffee_ls())


# about
@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run()
