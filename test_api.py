#!/usr/bin/env python3
"""
Script testing untuk API Sistem Pemantauan Lingkungan IoT
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000/api"

def test_get_devices():
    """Test mendapatkan semua perangkat"""
    print("=== Testing GET /api/devices ===")
    response = requests.get(f"{BASE_URL}/devices")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        devices = response.json()
        print(f"Jumlah perangkat: {len(devices)}")
        for device in devices:
            print(f"- {device['device_name']} ({device['device_id']})")
    print()

def test_get_device():
    """Test mendapatkan perangkat spesifik"""
    print("=== Testing GET /api/devices/dev001 ===")
    response = requests.get(f"{BASE_URL}/devices/dev001")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        device = response.json()
        print(f"Perangkat: {device['device_name']}")
        print(f"Lokasi: {device['location']}")
        print(f"Jumlah sensor: {len(device['sensors'])}")
    print()

def test_get_sensor_readings():
    """Test mendapatkan pembacaan sensor"""
    print("=== Testing GET /api/sensors/temp001/readings ===")
    response = requests.get(f"{BASE_URL}/sensors/temp001/readings?limit=5")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        readings = response.json()
        print(f"Jumlah pembacaan: {len(readings)}")
        for reading in readings[:3]:  # Show first 3
            print(f"- {reading['timestamp']}: {reading['value']} {reading['unit']}")
    print()

def test_get_device_readings():
    """Test mendapatkan pembacaan perangkat"""
    print("=== Testing GET /api/devices/dev001/readings ===")
    response = requests.get(f"{BASE_URL}/devices/dev001/readings?limit=10")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        readings = response.json()
        print(f"Jumlah pembacaan: {len(readings)}")
        # Group by sensor
        sensors = {}
        for reading in readings:
            sensor_id = reading['sensor_id']
            if sensor_id not in sensors:
                sensors[sensor_id] = []
            sensors[sensor_id].append(reading)
        
        for sensor_id, sensor_readings in sensors.items():
            print(f"- {sensor_id}: {len(sensor_readings)} pembacaan")
    print()

def test_get_latest_reading():
    """Test mendapatkan pembacaan terbaru"""
    print("=== Testing GET /api/sensors/temp001/latest ===")
    response = requests.get(f"{BASE_URL}/sensors/temp001/latest")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        reading = response.json()
        print(f"Pembacaan terbaru: {reading['value']} {reading['unit']}")
        print(f"Waktu: {reading['timestamp']}")
    print()

def test_add_reading():
    """Test menambah pembacaan baru"""
    print("=== Testing POST /api/readings ===")
    new_reading = {
        "device_id": "dev001",
        "sensor_id": "temp001",
        "sensor_type": "temperature",
        "value": 26.5,
        "unit": "°C"
    }
    response = requests.post(f"{BASE_URL}/readings", json=new_reading)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        reading = response.json()
        print(f"Pembacaan berhasil ditambahkan: {reading['value']} {reading['unit']}")
    print()

def test_add_device():
    """Test menambah perangkat baru"""
    print("=== Testing POST /api/devices ===")
    new_device = {
        "device_id": "dev003",
        "device_name": "Sensor Udara Ruang Meeting",
        "location": "Ruang Meeting",
        "description": "Sensor pemantauan kualitas udara di ruang meeting",
        "sensors": [
            {
                "sensor_id": "temp003",
                "type": "temperature",
                "unit": "°C",
                "description": "Sensor suhu"
            },
            {
                "sensor_id": "hum003",
                "type": "humidity",
                "unit": "%",
                "description": "Sensor kelembapan"
            }
        ]
    }
    response = requests.post(f"{BASE_URL}/devices", json=new_device)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        device = response.json()
        print(f"Perangkat berhasil ditambahkan: {device['device_name']}")
    print()

def test_get_stats():
    """Test mendapatkan statistik sistem"""
    print("=== Testing GET /api/stats ===")
    response = requests.get(f"{BASE_URL}/stats")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        stats = response.json()
        print(f"Total perangkat: {stats['total_devices']}")
        print(f"Total pembacaan: {stats['total_readings']}")
        print(f"Jumlah tipe sensor: {len(stats['latest_readings'])}")
        for sensor_type, reading in stats['latest_readings'].items():
            print(f"- {sensor_type}: {reading['value']} {reading['unit']}")
    print()

def test_time_range_queries():
    """Test query dengan rentang waktu"""
    print("=== Testing Time Range Queries ===")
    
    # Get readings from last hour
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=1)
    
    params = {
        'start_time': start_time.isoformat(),
        'end_time': end_time.isoformat(),
        'limit': 10
    }
    
    response = requests.get(f"{BASE_URL}/sensors/temp001/readings", params=params)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        readings = response.json()
        print(f"Pembacaan dalam 1 jam terakhir: {len(readings)}")
    print()

def run_all_tests():
    """Menjalankan semua test"""
    print("🚀 Memulai Testing API Sistem Pemantauan Lingkungan IoT")
    print("=" * 60)
    
    try:
        test_get_devices()
        test_get_device()
        test_get_sensor_readings()
        test_get_device_readings()
        test_get_latest_reading()
        test_add_reading()
        test_add_device()
        test_get_stats()
        test_time_range_queries()
        
        print("✅ Semua test selesai!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Tidak dapat terhubung ke server. Pastikan aplikasi Flask berjalan di http://localhost:5000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_all_tests() 