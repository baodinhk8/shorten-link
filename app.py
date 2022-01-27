import sqlite3 as sql
from flask_cors import CORS, cross_origin
from flask import Flask, request, render_template, redirect
import string    
import random 
import re
import time

app = Flask(__name__, template_folder='templates')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def Find(string):
  
    # findall() has been used 
    # with valid conditions for urls in string
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,string)      
    return [x[0] for x in url]

@app.route("/", methods=['GET', 'POST'])
@cross_origin()
def index():
    if request.method == 'POST':
        shorten_link=""
        url = request.form['origin']
        if len(Find(url))== 0:
            return render_template("index.html",shorten_link="No URL has been found")
        special=['!',"@","#","$","%","^","&","*","(",")","=","+","'",'"',"/","~"]
        custom = request.form['custom']
        for symbol in special:
            if symbol in custom:
                return render_template("index.html",shorten_link="Your string contain special symbol")
        custom = custom.lower()
        custom = custom.replace(" ", "_")
        with sql.connect("database.db") as con:
            cur = con.cursor()

            if custom == "":
                random.seed(time.time())
                ran = str(''.join(random.choices(string.ascii_uppercase + string.digits, k = 4)))

                # cur.execute("SELECT * FROM db WHERE shorten_url='"+ran+"'")

                # rows = cur.fetchall()

                # for row in rows:
                #     return a()

                cur.execute("INSERT INTO db VALUES ('"+url+"','"+ran+"',0)")
                shorten_link="Your new link is: https://ulrshorter.herokuapp.com/"+ran
            else:
                cur.execute("SELECT * FROM db WHERE shorten_url='"+custom+"'")

                rows = cur.fetchall()

                for row in rows:
                    return render_template("index.html",shorten_link="Your custom name have been taken")
                cur.execute("INSERT INTO db VALUES ('"+url+"','"+custom+"',0)")
                shorten_link="Your new link is: https://ulrshorter.herokuapp.com/"+custom
            
            con.commit()
            print(shorten_link)
            return render_template("index.html",shorten_link=shorten_link)

    return render_template("index.html")

@app.route('/<short_id>')
def redirect_url(short_id):
    with sql.connect("database.db") as con:
        cur = con.cursor()

        cur.execute("SELECT * FROM db WHERE shorten_url='"+short_id+"'")

        rows = cur.fetchall()

        for row in rows:
            return redirect(row[0])
    return(render_template("404.html"))

if __name__ == '__main__':
    app.run()
