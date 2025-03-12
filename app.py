from flask import Flask, request, jsonify
from otherStuff.db_setup import db  
from datetime import datetime
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///locations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

location = {}
current_direction = None
current_speed = 50
current_distance = None
optitrack_data = None

@app.route('/Optitracking_data', methods=['POST'])  # from OptiTrack
def reciev_Optitracking_data():
    global optitrack_data
    data = request.json.get('data')
    if not data:
        return jsonify({"status": "error", "message": "Invalid data"}), 400
    optitrack_data = data
    return jsonify({"status": "success", "Opti Location": optitrack_data}), 200
        
@app.route('/Optitracking_data_forward', methods=['GET']) #to triangle
def get_Optitracking_data():
	return jsonify({"Opti_data": optitrack_data}),200

@app.route('/speed', methods=['POST'])
def make_speed():
    global current_speed
    #speed = request.args.get('speed')
    speed = request.json.get('speed')
    if isinstance(speed, (int,float)) and speed <= 100 :
        current_speed = speed
        return jsonify({"status": "success", "speed": current_speed}), 200
    else :
        return jsonify({"status": "error", "message": "Invalid speed"}), 400

@app.route('/current_speed', methods=['GET'])
def get_current_speed():
    return jsonify({"speed": current_speed}), 200

@app.route('/move', methods=['POST'])
def move_robot():
    global current_direction
    direction = request.args.get('direction')
    if direction not in ['up', 'down', 'left', 'right', 'stop', 'up-left', 'up-right', 'down-left', 'down-right', 'circle', 'square', 'triangle', 'hexagon']:
        return jsonify({"status": "error", "message": "Invalid direction"}), 400
    current_direction = direction
    return jsonify({"status": "success", "direction": current_direction}), 200

@app.route('/current_direction', methods=['GET'])
def get_current_direction():
    return jsonify({"direction": current_direction}), 200

@app.route('/clear', methods=['DELETE'])
def clear_locations():
    try:
        db.session.query(Location).delete()
        db.session.commit()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/beacons', methods=['GET'])  #to triangle
def get_beacon_positions():
    return jsonify(device_positions), 200


@app.route('/beacons', methods=['POST'])
def update_beacon_positions():
    global device_positions
    data = request.get_json()
    device_positions = {
        "DC:C7:ED:2C:04:D1": (data["beacon1"]["x"], data["beacon1"]["y"]),
        "D1:DC:74:F2:C7:05": (data["beacon2"]["x"], data["beacon2"]["y"]),
        "D0:FB:A6:16:7D:AC": (data["beacon3"]["x"], data["beacon3"]["y"]),
        "C3:F0:97:50:8B:EA": (data["beacon4"]["x"], data["beacon4"]["y"])
    }
    return jsonify({"status": "success"}), 200

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Float, nullable=False)
    y = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/position', methods=['POST']) #from triangle
def receive_position():
    data = request.get_json()
    x = data.get('x')
    y = data.get('y')
    if x is None or y is None:
        return jsonify({"error": "Missing x or y coordinates"}), 400
    
    location["x"] = x
    location["y"] = y
    return jsonify({"message": "Location data saved"}), 200

@app.route('/locations', methods=['GET'])
def get_locations():
    return jsonify(location), 200

@app.route('/distance', methods=['POST'])
def receive_distance():
    global current_distance
    distance = request.json.get('distance')
    if isinstance(distance, (int, float)) and distance >= 0:
        current_distance = distance
        return jsonify({"status": "success", "distance": current_distance}), 200
    else:
        return jsonify({"status": "error", "message": "Invalid distance"}), 400

@app.route('/current_distance', methods=['GET'])
def get_current_distance():
    if current_distance is not None:
        return jsonify({"distance": current_distance}), 200
    else:
        return jsonify({"status": "error", "message": "No distance recorded"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
