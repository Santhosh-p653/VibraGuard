from flask import Flask, render_template, jsonify
from datetime import datetime
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vibration/history/30')
def vibration_history():
    now = datetime.now()
    readings = [
        {"timestamp": now.replace(microsecond=0).strftime("%Y-%m-%d %H:%M:%S"),
         "value": round(random.uniform(0, 10), 2)}
        for _ in range(30)
    ]
    return jsonify(readings)

if __name__ == '__main__':
    app.run(debug=True)
