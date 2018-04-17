from flask import Flask, render_template, redirect, request
app = Flask(__name__, static_url_path='/static')

@app.route("/")
def index():  
    # print(request.form["value"])
    return render_template('layout.html')

@app.route('/CA')
def state_ca():  
    return render_template('ca.html')

@app.route("/redirectpage", methods=['POST'])
def rederictPage():  
    return redirect(request.form["state"])
    # return render_template('layout.html')
# @app.route('/about')
# def about():    
#     html = '''        
#       <h1>About Jelly </h1>        
#       <p> This is my first ever Flask website! </p> 
#       <div>    
#       <img src="/static/IMG_1980.GIF" width=400 />
#       <div>     
#       <a href="/"> Go back home </a>

#       '''    
#     return html


# ctr = 0
# @app.route('/counter')
# def counter():    
#   global ctr    
#   ctr += 1    
#   return '<h3>' + str(ctr) + '</h3>'



if __name__ == '__main__':  
    print('starting Flask app', app.name)  
    app.run(debug=True)