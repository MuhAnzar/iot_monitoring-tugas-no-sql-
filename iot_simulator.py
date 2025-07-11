#!/usr/bin/env python3
"""
Simulator Perangkat IoT untuk Sistem Pemantauan Lingkungan
Mengirim data sensor secara periodik ke API
"""

import requests
import time
import random
import json
from datetime import datetime
import threading
from typing import Dict, List

class IoTSimulator:
    def __init__(self, api_base_url: str = "http://localhost:5000/api"):
        self.api_base_url = api_base_url
        self.devices = []
        self.running = False
        self.threads = []
        
    def add_device(self, device_config: Dict):
        """Menambah perangkat IoT ke simulator"""
        self.devices.append(device_config)
        print(f"✅ Perangkat {device_config['device_name']} ditambahkan ke simulator")
    
    def generate_sensor_value(self, sensor_type: str, base_value: float, variation: float = 0.1) -> float:
        """Generate nilai sensor yang realistis"""
        if sensor_type == "temperature":
            # Suhu bervariasi antara base_value ± variation
            value = base_value + random.uniform(-variation, variation)
            # Tambahkan tren harian (lebih dingin di malam hari)
            hour = datetime.now().hour
            if 22 <= hour or hour <= 6:  # Malam hari
                value -= 2
            elif 10 <= hour <= 16:  # Siang hari
                value += 3
        elif sensor_type == "humidity":
            # Kelembapan bervariasi dengan pola yang lebih kompleks
            value = base_value + random.uniform(-5, 5)
            # Kelembapan lebih tinggi di pagi dan malam
            hour = datetime.now().hour
            if 6 <= hour <= 8:  # Pagi
                value += 10
            elif 22 <= hour or hour <= 6:  # Malam
                value += 15
        elif sensor_type == "co2":
            # CO2 bervariasi berdasarkan aktivitas
            value = base_value + random.uniform(-20, 20)
            # CO2 lebih tinggi di jam kerja
            hour = datetime.now().hour
            if 8 <= hour <= 18:  # Jam kerja
                value += 100
        else:
            value = base_value + random.uniform(-variation, variation)
        
        return round(value, 2)
    
    def send_sensor_reading(self, device_id: str, sensor_id: str, sensor_type: str, value: float, unit: str):
        """Mengirim pembacaan sensor ke API"""
        reading_data = {
            "device_id": device_id,
            "sensor_id": sensor_id,
            "sensor_type": sensor_type,
            "value": value,
            "unit": unit
        }
        
        try:
            response = requests.post(f"{self.api_base_url}/readings", json=reading_data)
            if response.status_code == 201:
                print(f"📡 {device_id}/{sensor_id}: {value} {unit}")
            else:
                print(f"❌ Error mengirim data: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Error koneksi: {e}")
    
    def simulate_device(self, device_config: Dict):
        """Simulasi perangkat IoT individual"""
        device_id = device_config["device_id"]
        device_name = device_config["device_name"]
        sensors = device_config["sensors"]
        
        print(f"🚀 Memulai simulasi perangkat: {device_name}")
        
        while self.running:
            for sensor in sensors:
                # Generate nilai sensor
                value = self.generate_sensor_value(
                    sensor["type"], 
                    sensor.get("base_value", 25),
                    sensor.get("variation", 2)
                )
                
                # Kirim data ke API
                self.send_sensor_reading(
                    device_id,
                    sensor["sensor_id"],
                    sensor["type"],
                    value,
                    sensor["unit"]
                )
            
            # Tunggu interval sebelum pembacaan berikutnya
            time.sleep(device_config.get("interval", 30))  # Default 30 detik
    
    def start_simulation(self):
        """Memulai simulasi semua perangkat"""
        if not self.devices:
            print("❌ Tidak ada perangkat yang dikonfigurasi")
            return
        
        self.running = True
        print(f"🎯 Memulai simulasi {len(self.devices)} perangkat IoT...")
        
        # Buat thread untuk setiap perangkat
        for device_config in self.devices:
            thread = threading.Thread(
                target=self.simulate_device,
                args=(device_config,),
                daemon=True
            )
            thread.start()
            self.threads.append(thread)
        
        print("✅ Simulasi berjalan. Tekan Ctrl+C untuk berhenti.")
        
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop_simulation()
    
    def stop_simulation(self):
        """Menghentikan simulasi"""
        print("\n🛑 Menghentikan simulasi...")
        self.running = False
        
        # Tunggu semua thread selesai
        for thread in self.threads:
            thread.join(timeout=5)
        
        print("✅ Simulasi dihentikan")

def create_sample_devices():
    """Membuat konfigurasi perangkat sample"""
    devices = [
        {
            "device_id": "dev001",
            "device_name": "Sensor Udara Ruang Lab",
            "location": "Ruang Lab",
            "interval": 30,  # 30 detik
            "sensors": [
                {
                    "sensor_id": "temp001",
                    "type": "temperature",
                    "unit": "°C",
                    "base_value": 25,
                    "variation": 2,
                    "description": "Sensor suhu"
                },
                {
                    "sensor_id": "hum001",
                    "type": "humidity",
                    "unit": "%",
                    "base_value": 60,
                    "variation": 10,
                    "description": "Sensor kelembapan"
                },
                {
                    "sensor_id": "co2_001",
                    "type": "co2",
                    "unit": "ppm",
                    "base_value": 400,
                    "variation": 50,
                    "description": "Sensor CO2"
                }
            ]
        },
        {
            "device_id": "dev002",
            "device_name": "Sensor Udara Ruang Server",
            "location": "Ruang Server",
            "interval": 45,  # 45 detik
            "sensors": [
                {
                    "sensor_id": "temp002",
                    "type": "temperature",
                    "unit": "°C",
                    "base_value": 22,
                    "variation": 1.5,
                    "description": "Sensor suhu"
                },
                {
                    "sensor_id": "hum002",
                    "type": "humidity",
                    "unit": "%",
                    "base_value": 45,
                    "variation": 8,
                    "description": "Sensor kelembapan"
                }
            ]
        },
        {
            "device_id": "dev003",
            "device_name": "Sensor Udara Ruang Meeting",
            "location": "Ruang Meeting",
            "interval": 60,  # 60 detik
            "sensors": [
                {
                    "sensor_id": "temp003",
                    "type": "temperature",
                    "unit": "°C",
                    "base_value": 24,
                    "variation": 3,
                    "description": "Sensor suhu"
                },
                {
                    "sensor_id": "hum003",
                    "type": "humidity",
                    "unit": "%",
                    "base_value": 55,
                    "variation": 12,
                    "description": "Sensor kelembapan"
                },
                {
                    "sensor_id": "co2_003",
                    "type": "co2",
                    "unit": "ppm",
                    "base_value": 450,
                    "variation": 100,
                    "description": "Sensor CO2"
                }
            ]
        }
    ]
    return devices

def main():
    """Main function untuk menjalankan simulator"""
    print("🌐 IoT Simulator - Sistem Pemantauan Lingkungan")
    print("=" * 50)
    
    # Buat simulator
    simulator = IoTSimulator()
    
    # Tambahkan perangkat sample
    devices = create_sample_devices()
    for device in devices:
        simulator.add_device(device)
    
    print(f"\n📊 Konfigurasi Simulator:")
    print(f"- Jumlah perangkat: {len(devices)}")
    print(f"- API URL: {simulator.api_base_url}")
    print(f"- Interval pengiriman: 30-60 detik")
    print(f"- Sensor types: temperature, humidity, co2")
    
    print("\n🎯 Memulai simulasi...")
    print("💡 Tips: Buka dashboard di http://localhost:5000 untuk melihat data real-time")
    print("🛑 Tekan Ctrl+C untuk menghentikan simulasi")
    
    # Jalankan simulasi
    simulator.start_simulation()

if __name__ == "__main__":
    main() 