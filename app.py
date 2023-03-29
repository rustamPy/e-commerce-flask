import urllib.parse

from flask import Flask, render_template, request

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


    class Cart(db.Model):
        __tablename__ = 'cart_t'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(50))
        quantity = db.Column(db.Integer)
        rank = db.Column(db.Integer)
        price = db.Column(db.Float)


    class GetCoffee:
        def get_coffee_ls(self):
            coffee_ls = Coffee.query.all()
            return [(i.id, i.name, i.quantity, i.rank, i.price) for i in coffee_ls]


    coffee_obj = GetCoffee()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/menu', methods=['GET', 'POST'])
def menu():
    if request.method == 'POST':
        pass
    else:
        return render_template('menu.html', items=coffee_obj.get_coffee_ls())


# about
@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run()
