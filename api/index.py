from flask import Flask
import time

app = Flask(__name__)

@app.route("/")
def hello_world():
    return {
        "status": "OK"
    }

@app.route("/part-a")
def partA():
    return {
        "timestamp": int(time.time()),
        "test_type": "Part A"
    }

@app.route("/part-b")
def partB():
    return {
        "timestamp": int(time.time()),
        "test_type": "Part B"
    }