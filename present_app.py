from flask import Flask, render_template, request, redirect
# import model

app = Flask(__name__)
@app.route("/")
def index():
    return '''<div>
            <a href="https://plot.ly/~jellyjellyz/57/?share_key=kGmIDZjmLrn3vUmScnxmFL" target="_blank" title="jobs in America" style="display: block; text-align: center;"><img src="https://plot.ly/~jellyjellyz/57.png?share_key=kGmIDZjmLrn3vUmScnxmFL" alt="jobs in America" style="max-width: 100%;width: 1300px;"  width="1300" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
            <script data-plotly="jellyjellyz:57" sharekey-plotly="kGmIDZjmLrn3vUmScnxmFL" src="https://plot.ly/embed.js" async></script>
        </div>
        '''



if __name__ == '__main__':  
    print('starting Flask app', app.name)  
    app.run(debug=True)