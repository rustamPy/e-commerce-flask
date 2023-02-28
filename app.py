from flask import Flask, render_template

app = Flask(__name__)


@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
