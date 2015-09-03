from flask import Flask, g, render_template, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('default/index.html')


@app.route('/team')
def team():
    return render_template('misc/the-team.html')


@app.route('/login')
def login():
    return render_template('user/login.html')


@app.route('/register', methods=('GET', 'POST'))
def register():
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
