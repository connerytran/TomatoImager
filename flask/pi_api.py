
from flask import Flask, jsonify


app = Flask(__name__)

@app.route('/status', methods=['GET'])
def get_status():
  status = {"message": "Pi is online and ready",
            "device": "Pi3: Steve"}
  return jsonify(status)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)