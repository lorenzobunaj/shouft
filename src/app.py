from core import *
from flask import Flask, request, redirect, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# app config
app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri="memory://"
)

# render index.html
@app.route("/")
def index():
    return render_template("index.html")

# render about.html
@app.route("/about")
def about():
    return render_template("about.html")

# return the refer
@app.route("/api/url/add", methods=["POST"])
@limiter.limit("5/30second")
def add():
    addToDb = db.addUrl(request.get_json()["url"])

    if addToDb == 0:
        return {"status": 0x0}

    elif addToDb == 2:
        return {"status": 0x2}

    else:
        return {"status": addToDb}

# redirect
@app.route('/<short_url>', methods=["GET"])
@limiter.limit("10/30second")
def get(short_url):

    getToDb = db.getUrl(short_url)

    if getToDb == 0:
        return {"status":  0x0}

    elif getToDb == 3:
        return {"status": 0x3}

    else:
        return redirect(getToDb)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port="3000")