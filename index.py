from flask import Flask, render_template
import crawler_dcard as dcard

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html",imgDisplay='none')

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
