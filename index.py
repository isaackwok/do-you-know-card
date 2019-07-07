from flask import Flask, render_template
import crawler_dcard as dcard

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html",imgDisplay='none')

@app.route("/f/")
def all():
    resultArr = dcard.analyse("")
    print(resultArr[0])
    return render_template("index.html",tfidf=resultArr[0],textrank=resultArr[1],imgDisplay='block')

@app.route("/f/<key>")
def kanban(key):
    resultArr = dcard.analyse(key)
    print(resultArr[0])
    return render_template("index.html",tfidf=resultArr[0],textrank=resultArr[1],imgDisplay='block')

if __name__ == "__main__":
    app.run(
        host= '0.0.0.0',
        port=8080
    )
# ----
# from quart import Quart, websocket
# from flask import Flask, render_template
# import crawler_dcard as dcard

# app = Quart(__name__)


# @app.route('/')
# async def index():
#     return render_template("index.html")


# @app.route('/f/')
# async def all():
#     resultArr = dcard.analyse("")
#     print(resultArr[0])
#     return render_template("index.html", tfidf=resultArr[0], textrank=resultArr[1])


# @app.route('/f/<key>')
# async def kanban(key):
#     resultArr = dcard.analyse(key)
#     print(resultArr[0])
#     return render_template("index.html", tfidf=resultArr[0], textrank=resultArr[1])

# app.run(
#     host='0.0.0.0'
# )

# --
