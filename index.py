import crawler_dcard as dcard
import logging
import os
from flask import Flask, render_template
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

if not os.path.exists('log'):
    os.makedirs('log')
logging.basicConfig(
    filename='log/debug.log',
     level=logging.DEBUG,
     format='[%(asctime)s][%(levelname)s][%(name)s]: %(message)s'
    )

@app.route("/")
def index():
    return render_template("index.html",imgDisplay='none')

@app.route("/f/<key>")
def kanban(key):
    resultArr = dcard.analyse(key)
    return render_template("index.html",tfidf=resultArr[0],textrank=resultArr[1],imgDisplay='block', imgsrc=resultArr[2])

if __name__ == "__main__":
    app.run(
        host= '0.0.0.0',
        port=8080
    )
# ----
