###main presentaion web appication.
from flask import Flask, render_template, redirect, request
app = Flask(__name__, static_url_path='/static')

@app.route("/")
def index():  
    # print(request.form["value"])
    return render_template('layout.html')

@app.route("/redirectpage", methods=['POST'])
def rederictPage():  
    return redirect(request.form["state"])

@app.route('/ca')
def state_ca():
    return render_template('ca.html')

@app.route('/mi')
def state_mi():  
    return render_template('mi.html')

@app.route('/fl')
def state_fl():  
    return render_template('fl.html')

@app.route('/all')
def all():  
    return render_template('all.html')

@app.route('/lag')
def lag():  
    return render_template('lag.html')

@app.route('/numofjobsbystate')
def numofjobsbystate():  
    return render_template('numofjobsbystate.html')

if __name__ == '__main__':  
    print('starting Flask app', app.name)  
    app.run(debug=True)