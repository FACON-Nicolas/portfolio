from flask import Flask, render_template, redirect

app = Flask(__name__)


@app.route("/")
def main():
    return redirect('/portfolio')


@app.route('/portfolio')
def portfolio():
    return render_template('home.html', title='portfolio')


if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()
