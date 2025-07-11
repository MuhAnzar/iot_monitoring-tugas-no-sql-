from flask import Flask, render_template, request, jsonify, send_file, Response
from pymongo import MongoClient
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from flask_cors import CORS
import json
import csv
from io import StringIO, BytesIO
from pymongo import ASCENDING
import math

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# MongoDB connection
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    # Test connection
    client.server_info()
    db = client['iot_monitoring']
    print("✅ MongoDB terhubung!")
except Exception as e:
    print(f"⚠️  MongoDB tidak terhubung: {e}")
    print("💡 Sistem akan berjalan dengan data in-memory")
    # Fallback ke in-memory storage
    db = None

# Initialize database with sample data
def init_database():
    """Initialize database with sample IoT devices and sensor data"""
    
    # Clear existing data
    db.devices.drop()
    db.sensor_readings.drop()
    
    # Sample devices
    devices = [
        {
            "device_id": "dev001",
            "device_name": "Sensor Udara Ruang Lab",
            "location": "Ruang Lab",
            "description": "Sensor pemantauan kualitas udara di ruang laboratorium",
            "sensors": [
                {
                    "sensor_id": "temp001",
                    "type": "temperature",
                    "unit": "°C",
                    "description": "Sensor suhu"
                },
                {
                    "sensor_id": "hum001", 
                    "type": "humidity",
                    "unit": "%",
                    "description": "Sensor kelembapan"
                },
                {
                    "sensor_id": "co2_001",
                    "type": "co2",
                    "unit": "ppm",
                    "description": "Sensor CO2"
                }
            ]
        },
        {
            "device_id": "dev002",
            "device_name": "Sensor Udara Ruang Server",
            "location": "Ruang Server",
            "description": "Sensor pemantauan suhu dan kelembapan di ruang server",
            "sensors": [
                {
                    "sensor_id": "temp002",
                    "type": "temperature",
                    "unit": "°C",
                    "description": "Sensor suhu"
                },
                {
                    "sensor_id": "hum002",
                    "type": "humidity", 
                    "unit": "%",
                    "description": "Sensor kelembapan"
                }
            ]
        }
    ]
    
    # Insert devices
    db.devices.insert_many(devices)
    
    # Generate sample sensor readings for the last 24 hours
    now = datetime.now()
    sensor_readings = []
    
    for device in devices:
        for sensor in device['sensors']:
            # Generate readings every 5 minutes for the last 24 hours
            for i in range(288):  # 24 hours * 12 readings per hour
                timestamp = now - timedelta(minutes=5*i)
                
                # Generate realistic sensor values
                if sensor['type'] == 'temperature':
                    base_temp = 25 if device['device_id'] == 'dev001' else 22
                    value = base_temp + (i % 10) * 0.5  # Varying temperature
                elif sensor['type'] == 'humidity':
                    base_humidity = 60 if device['device_id'] == 'dev001' else 45
                    value = base_humidity + (i % 15) * 2  # Varying humidity
                elif sensor['type'] == 'co2':
                    base_co2 = 400 + (i % 20) * 10  # Varying CO2 levels
                    value = base_co2
                
                reading = {
                    "device_id": device['device_id'],
                    "sensor_id": sensor['sensor_id'],
                    "sensor_type": sensor['type'],
                    "timestamp": timestamp,
                    "value": round(value, 2),
                    "unit": sensor['unit']
                }
                sensor_readings.append(reading)
    
    # Insert sensor readings
    db.sensor_readings.insert_many(sensor_readings)
    
    print("Database initialized with sample data!")

# Routes
@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/devices')
def get_devices():
    """Get all devices"""
    devices = list(db.devices.find({}, {'_id': 0}))
    return jsonify(devices)

@app.route('/api/devices/<device_id>')
def get_device(device_id):
    """Get specific device by ID"""
    device = db.devices.find_one({"device_id": device_id}, {'_id': 0})
    if device:
        return jsonify(device)
    return jsonify({"error": "Device not found"}), 404

@app.route('/api/sensors/<sensor_id>/readings')
def get_sensor_readings(sensor_id):
    """Get sensor readings for a specific sensor"""
    # Get query parameters
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    limit = int(request.args.get('limit', 100))
    
    # Build query
    query = {"sensor_id": sensor_id}
    
    if start_time:
        query["timestamp"] = {"$gte": datetime.fromisoformat(start_time)}
    if end_time:
        if "timestamp" in query:
            query["timestamp"]["$lte"] = datetime.fromisoformat(end_time)
        else:
            query["timestamp"] = {"$lte": datetime.fromisoformat(end_time)}
    
    readings = list(db.sensor_readings.find(
        query, 
        {'_id': 0}
    ).sort("timestamp", -1).limit(limit))
    
    return jsonify(readings)

@app.route('/api/devices/<device_id>/readings')
def get_device_readings(device_id):
    """Get all sensor readings for a device, with pagination support"""
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    limit = int(request.args.get('limit', 100))
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    
    query = {"device_id": device_id}
    
    if start_time:
        query["timestamp"] = {"$gte": datetime.fromisoformat(start_time)}
    if end_time:
        if "timestamp" in query:
            query["timestamp"]["$lte"] = datetime.fromisoformat(end_time)
        else:
            query["timestamp"] = {"$lte": datetime.fromisoformat(end_time)}
    
    skip = (page - 1) * per_page
    readings_cursor = db.sensor_readings.find(
        query, 
        {'_id': 0}
    ).sort("timestamp", -1).skip(skip).limit(per_page)
    readings = list(readings_cursor)
    total = db.sensor_readings.count_documents(query)
    
    return jsonify({
        "data": readings,
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": (total + per_page - 1) // per_page
    })

@app.route('/api/sensors/<sensor_id>/latest')
def get_latest_reading(sensor_id):
    reading = db.sensor_readings.find(
        {"sensor_id": sensor_id},
        {'_id': 0}
    ).sort("timestamp", -1).limit(1)
    reading = list(reading)
    if reading:
        return jsonify(reading[0])
    return jsonify({"error": "No readings found"}), 404

@app.route('/api/readings', methods=['POST'])
def add_reading():
    """Add new sensor reading"""
    data = request.json
    
    required_fields = ['device_id', 'sensor_id', 'sensor_type', 'value', 'unit']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    reading = {
        "device_id": data['device_id'],
        "sensor_id": data['sensor_id'],
        "sensor_type": data['sensor_type'],
        "timestamp": datetime.now(),
        "value": float(data['value']),
        "unit": data['unit']
    }
    
    result = db.sensor_readings.insert_one(reading)
    reading['_id'] = str(result.inserted_id)
    
    return jsonify(reading), 201

@app.route('/api/devices', methods=['POST'])
def add_device():
    """Add new device"""
    data = request.json
    
    if 'device_id' not in data or 'device_name' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    # Check if device already exists
    existing = db.devices.find_one({"device_id": data['device_id']})
    if existing:
        return jsonify({"error": "Device ID already exists"}), 409
    
    device = {
        "device_id": data['device_id'],
        "device_name": data['device_name'],
        "location": data.get('location', ''),
        "description": data.get('description', ''),
        "sensors": data.get('sensors', [])
    }
    
    result = db.devices.insert_one(device)
    device['_id'] = str(result.inserted_id)
    
    return jsonify(device), 201

@app.route('/api/stats')
def get_stats():
    """Get system statistics"""
    total_devices = db.devices.count_documents({})
    total_readings = db.sensor_readings.count_documents({})
    
    # Get latest readings for each sensor type
    latest_readings = {}
    sensor_types = db.sensor_readings.distinct("sensor_type")
    
    for sensor_type in sensor_types:
        latest = db.sensor_readings.find(
            {"sensor_type": sensor_type}, 
            {'_id': 0}
        ).sort("timestamp", -1).limit(1)
        latest = list(latest)
        if latest:
            latest = latest[0]
        else:
            latest = None
        if latest:
            latest_readings[sensor_type] = latest
    
    stats = {
        "total_devices": total_devices,
        "total_readings": total_readings,
        "latest_readings": latest_readings
    }
    
    return jsonify(stats)

@app.route('/api/devices/<device_id>/readings/export')
def export_device_readings_csv(device_id):
    """Export all sensor readings for a device as CSV"""
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    query = {"device_id": device_id}
    if start_time:
        query["timestamp"] = {"$gte": datetime.fromisoformat(start_time)}
    if end_time:
        if "timestamp" in query:
            query["timestamp"]["$lte"] = datetime.fromisoformat(end_time)
        else:
            query["timestamp"] = {"$lte": datetime.fromisoformat(end_time)}
    readings = list(db.sensor_readings.find(query, {'_id': 0}).sort("timestamp", -1))
    # Prepare CSV
    si = StringIO()
    writer = csv.DictWriter(si, fieldnames=["device_id", "sensor_id", "sensor_type", "timestamp", "value", "unit"])
    writer.writeheader()
    for r in readings:
        # Convert timestamp to ISO string if needed
        if isinstance(r["timestamp"], (str, bytes)):
            pass
        else:
            r["timestamp"] = r["timestamp"].isoformat()
        writer.writerow(r)
    output = si.getvalue()
    si.close()
    return Response(
        output,
        mimetype="text/csv",
        headers={
            "Content-Disposition": f"attachment;filename=readings_{device_id}.csv"
        }
    )

@app.route('/api/devices/<device_id>/readings/range')
def get_readings_in_range(device_id):
    start = request.args.get('start')
    end = request.args.get('end')
    query = {'device_id': device_id}
    if start and end:
        query['timestamp'] = {'$gte': start, '$lte': end}
    readings = list(db.sensor_readings.find(query))
    for r in readings:
        r['_id'] = str(r['_id'])
    return jsonify(readings)

@app.route('/api/devices/<device_id>/sensors/<sensor_id>/stats')
def get_sensor_stats(device_id, sensor_id):
    start = request.args.get('start')
    end = request.args.get('end')
    match = {
        'device_id': device_id,
        'sensor_id': sensor_id
    }
    if start and end:
        match['timestamp'] = {'$gte': start, '$lte': end}
    pipeline = [
        {'$match': match},
        {'$group': {
            '_id': None,
            'avg': {'$avg': '$value'},
            'min': {'$min': '$value'},
            'max': {'$max': '$value'},
            'stddev': {'$stdDevPop': '$value'},
            'count': {'$sum': 1}
        }}
    ]
    result = list(db.sensor_readings.aggregate(pipeline))
    return jsonify(result[0] if result else {})

@app.route('/api/alerts/threshold')
def get_devices_exceeding_threshold():
    sensor_type = request.args.get('type')
    threshold = float(request.args.get('threshold'))
    start = request.args.get('start')
    end = request.args.get('end')
    match = {'sensor_type': sensor_type, 'value': {'$gt': threshold}}
    if start and end:
        match['timestamp'] = {'$gte': start, '$lte': end}
    pipeline = [
        {'$match': match},
        {'$group': {'_id': '$device_id', 'max_value': {'$max': '$value'}}}
    ]
    result = list(db.sensor_readings.aggregate(pipeline))
    return jsonify(result)

@app.route('/api/report')
def api_report():
    device_id = request.args.get('device_id')
    sensor_id = request.args.get('sensor_id')
    start = request.args.get('start')
    end = request.args.get('end')
    threshold = request.args.get('threshold', type=float)
    # Query readings
    query = {'device_id': device_id, 'sensor_id': sensor_id}
    if start and end:
        query['timestamp'] = {'$gte': start, '$lte': end}
    readings = list(db.sensor_readings.find(query)) # Changed db.readings to db.sensor_readings
    # Stats
    values = [r['value'] for r in readings]
    stats = {
        'avg': sum(values)/len(values) if values else None,
        'min': min(values) if values else None,
        'max': max(values) if values else None,
        'stddev': (sum((v - (sum(values)/len(values)))**2 for v in values)/len(values))**0.5 if values else None,
        'count': len(values)
    }
    # Exceed threshold
    exceed = []
    if threshold is not None:
        max_value = max(values) if values else None
        if max_value and max_value > threshold:
            exceed.append({'device_id': device_id, 'max_value': max_value})
    # Format readings
    for r in readings:
        r['_id'] = str(r['_id'])
    return jsonify({'stats': stats, 'exceed': exceed, 'readings': readings})

@app.route('/api/report/download')
def api_report_download():
    device_id = request.args.get('device_id')
    sensor_id = request.args.get('sensor_id')
    start = request.args.get('start')
    end = request.args.get('end')
    threshold = request.args.get('threshold', type=float)
    query = {'device_id': device_id, 'sensor_id': sensor_id}
    if start and end:
        query['timestamp'] = {'$gte': start, '$lte': end}
    readings = list(db.sensor_readings.find(query))
    # CSV
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['timestamp', 'value'])
    for r in readings:
        writer.writerow([r['timestamp'], r['value']])
    # ENCODE ke BytesIO sebelum dikirim
    mem = BytesIO()
    mem.write(output.getvalue().encode('utf-8'))
    mem.seek(0)
    output.close()
    return send_file(mem, mimetype='text/csv', as_attachment=True, download_name='laporan.csv')

if __name__ == '__main__':
    # Initialize database with sample data
    init_database()
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000) 