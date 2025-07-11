#!/usr/bin/env python3
"""
Script untuk menjalankan IoT Simulator terpisah
"""

import time
import threading
from iot_simulator import IoTSimulator, create_sample_devices

def main():
    """Main function untuk menjalankan IoT Simulator"""
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