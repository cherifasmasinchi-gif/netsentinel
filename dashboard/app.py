from flask import Flask, render_template
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from db.database import get_all_devices

app = Flask(__name__)


@app.route("/")
def index():
    devices = get_all_devices()
    return render_template("index.html", devices=devices)


if __name__ == "__main__":
    app.run(debug=True)
    