# coding: utf-8

from flask import Flask
from flask import request
from flask import session

app = Flask(__name__)
app.config.update({"SECRET_KEY": "abcde"})
@app.route("/")
def index():
    _id = request.args.get("id")
    print _id
    try:
        session["id"] = _id
        return "i am index"
    except Exception as e:
        print str(e)
        return 'serve error'

if __name__ == '__main__':
    with app.test_client() as c:
        rv = c.get('/?id=1')
        print rv
        print type(rv)
        print dir(rv)
        print session["id"]