import urllib

from flask import Flask, render_template

import pyodbc
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

conn_str = "DRIVER={SQL Server}; SERVER=forkoffee.database.windows.net; DATABASE=mydb;UID=drmohm@forkoffee; PWD=Ferum@1313"
params = urllib.parse.quote_plus(conn_str)

# initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecret'
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# extensions
db = SQLAlchemy(app)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# about
@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run()
