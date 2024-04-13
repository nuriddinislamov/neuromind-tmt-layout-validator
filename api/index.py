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
    return {
        "timestamp": int(time.time()),
        "test_type": "Part A",
        "layout": json.dump(
                                [
                        [518, 331],
                        [429, 389],
                        [410, 390],
                        [595, 464],
                        [608, 164],
                        [379, 194],
                        [506, 247],
                        [342, 313],
                        [254, 393],
                        [266, 486],
                        [361, 451],
                        [430, 557],
                        [80, 542],
                        [197, 304],
                        [55, 342],
                        [57, 18],
                        [64, 66],
                        [172, 126],
                        [242, 58],
                        [262, 192],
                        [445, 104],
                        [360, 49],
                        [371, 43],
                        [578, 47],
                        [720, 108]
                        # [767, 531],
                        # [675, 348],
                        # [635, 521]
                    ]
        )
    }

@app.route("/part-b")
def partB():
    return {
        "timestamp": int(time.time()),
        "test_type": "Part B"
    }