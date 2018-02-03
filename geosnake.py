from alchemia import DBHelper 
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, session 
from flask import make_response 
import datetime 
import os


app = Flask(__name__)
DB = DBHelper()
app.secret_key = os.urandom(24)


@app.route("/")
def home():
    try:
        lastSourceId = session.get('lastSourceId', None)
        lastSource = DB.getLastSource(lastSourceId)
        destinations = DB.getDestinations(lastSourceId)
    except Exception as e:
        print("home error: ", e)
    return render_template("home.html", data=[lastSource, destinations])


@app.route("/add", methods=["POST"])
def add():
    try:
        street = request.form.get("street")
        house_number = request.form.get("house_number")
        city = request.form.get("city")
        post_code = request.form.get("post_code")
        lastSourceId=DB.checkSource(post_code, city, street, house_number)
        if lastSourceId:
            session['lastSourceId']=lastSourceId[0]
            DB.calculateDistance(lastSourceId[0])
        else:
            session['lastSourceId']=None
            DB.insertSource(post_code, city, street, house_number)
            DB.calculateDistance()
    except Exception as e:
        print("add error: ", e)
    return redirect('/')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
