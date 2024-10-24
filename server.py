from flask import Flask, jsonify
import time
import random

app = Flask(__name__)

# Configurable delay for the video translation to complete
config = {
    "start_time": time.time(),
    "delay": 10,  # Simulate a 10-second delay before completion
    "error_chance": 0.1  # 10% chance of error
}

@app.route('/status', methods=['GET'])
def get_status():
    elapsed_time = time.time() - config["start_time"]
    
    if elapsed_time < config["delay"]:
        return jsonify({"result": "pending"})
    else:
        if random.random() < config["error_chance"]:
            return jsonify({"result": "error"})
        else:
            return jsonify({"result": "completed"})

if __name__ == '__main__':
    app.run(debug=True)
