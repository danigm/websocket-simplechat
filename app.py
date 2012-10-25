#!/usr/bin/env python2

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('app.html')

if __name__ == "__main__":
    app.run()
