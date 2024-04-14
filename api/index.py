import time
import json
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return {
        "timestamp": int(time.time()),
        "status": "OK",
        "student_id": "2117032",
        "author": "Nuriddin Islamov",
        "instructions": "Use one of the available endpoints and send a GET request to them. You will receive a valid TMT layout back in response. If it takes too long to respond, send the request again.",
        "available_endpoints": [
            "/part-a",
            "/part-b"
        ],
        "descriptions": {
            "/part-a": "The layout for Trail Making Test part A",
            "/part-b": "The layout for Trail Making Test part B"
        },
        "github": "https://github.com/nuriddinislamov/neuromind-tmt-layout-validator"
    }

@app.route("/part-a")
def partA():
    layout = [(992, 749), (757, 621), (613, 504), (666, 893), (285, 834), (229, 892), (533, 920), (794, 873), (670, 635), (755, 845), (174, 746), (324, 333), (386, 280), (499, 117), (530, 118), (490, 451), (425, 612), (144, 713), (451, 477), (876, 142)]
    return {
        "timestamp": int(time.time()),
        "test_type": "Part A",
        "num_of_nodes": len(layout),
        "grid_size": 1024,
        "layout": layout
    }

@app.route("/part-b")
def partB():
    return {
        "timestamp": int(time.time()),
        "test_type": "Part B"
    }