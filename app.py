from flask import Flask, render_template

import pyodbc

app = Flask(__name__)

conn_str = "DRIVER={SQL Server}; SERVER=forkoffee.database.windows.net; DATABASE=mydb;UID=drmohm@forkoffee; PWD=Ferum@1313"
conn = pyodbc.connect(conn_str)

cursor = conn.cursor()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# about
@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run()
