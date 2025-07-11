#!/usr/bin/env python3
"""
Script untuk menjalankan Sistem Pemantauan Lingkungan IoT
Menjalankan semua komponen: Flask API, IoT Simulator, dan Dashboard
"""

import subprocess
import time
import threading
import sys
import os
from datetime import datetime

class IoTSystemRunner:
    def __init__(self):
        self.processes = {}
        self.running = False
        
    def check_dependencies(self):
        """Cek apakah semua dependensi terinstall"""
        print("🔍 Memeriksa dependensi...")
        
        required_packages = [
            'flask', 'pymongo', 'requests', 'pandas', 
            'numpy', 'matplotlib', 'seaborn'
        ]
        
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package)
                print(f"✅ {package}")
            except ImportError:
                missing_packages.append(package)
                print(f"❌ {package} - TIDAK TERINSTALL")
        
        if missing_packages:
            print(f"\n⚠️  Dependensi yang hilang: {', '.join(missing_packages)}")
            print("💡 Jalankan: pip install -r requirements.txt")
            return False
        
        print("✅ Semua dependensi terinstall!")
        return True
    
    def check_mongodb(self):
        """Cek koneksi MongoDB"""
        print("\n🔍 Memeriksa koneksi MongoDB...")
        
        try:
            from pymongo import MongoClient
            client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
            client.server_info()
            print("✅ MongoDB terhubung!")
            return True
        except Exception as e:
            print(f"❌ MongoDB tidak dapat dihubungi: {e}")
            print("💡 Pastikan MongoDB berjalan di localhost:27017")
            return False
    
    def start_flask_app(self):
        """Menjalankan aplikasi Flask"""
        print("\n🚀 Menjalankan Flask API...")
        
        try:
            process = subprocess.Popen(
                [sys.executable, 'app.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.processes['flask'] = process
            
            # Tunggu sebentar untuk memastikan Flask berjalan
            time.sleep(3)
            
            if process.poll() is None:
                print("✅ Flask API berjalan di http://localhost:5000")
                return True
            else:
                stdout, stderr = process.communicate()
                print(f"❌ Flask API gagal dijalankan: {stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error menjalankan Flask: {e}")
            return False
    
    def start_iot_simulator(self):
        """Menjalankan IoT Simulator"""
        print("\n🌐 Menjalankan IoT Simulator...")
        
        try:
            process = subprocess.Popen(
                [sys.executable, 'iot_simulator.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.processes['simulator'] = process
            
            # Tunggu sebentar untuk memastikan simulator berjalan
            time.sleep(2)
            
            if process.poll() is None:
                print("✅ IoT Simulator berjalan")
                return True
            else:
                stdout, stderr = process.communicate()
                print(f"❌ IoT Simulator gagal dijalankan: {stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error menjalankan IoT Simulator: {e}")
            return False
    
    def run_data_analysis(self):
        """Menjalankan analisis data"""
        print("\n📊 Menjalankan analisis data...")
        
        try:
            result = subprocess.run(
                [sys.executable, 'data_analysis.py'],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                print("✅ Analisis data selesai!")
                print(result.stdout)
            else:
                print(f"❌ Analisis data gagal: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print("⏰ Analisis data timeout (60 detik)")
        except Exception as e:
            print(f"❌ Error menjalankan analisis data: {e}")
    
    def run_api_tests(self):
        """Menjalankan test API"""
        print("\n🧪 Menjalankan test API...")
        
        try:
            result = subprocess.run(
                [sys.executable, 'test_api.py'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                print("✅ Test API berhasil!")
                print(result.stdout)
            else:
                print(f"❌ Test API gagal: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print("⏰ Test API timeout (30 detik)")
        except Exception as e:
            print(f"❌ Error menjalankan test API: {e}")
    
    def monitor_processes(self):
        """Monitor proses yang berjalan"""
        while self.running:
            for name, process in self.processes.items():
                if process.poll() is not None:
                    print(f"⚠️  Proses {name} berhenti (exit code: {process.returncode})")
            
            time.sleep(5)
    
    def start_system(self):
        """Menjalankan seluruh sistem"""
        print("🌐 SISTEM PEMANTAUAN LINGKUNGAN IoT")
        print("=" * 50)
        
        # Cek dependensi
        if not self.check_dependencies():
            return False
        
        # Cek MongoDB
        if not self.check_mongodb():
            return False
        
        # Jalankan Flask API
        if not self.start_flask_app():
            return False
        
        # Jalankan test API
        self.run_api_tests()
        
        # Jalankan IoT Simulator
        if not self.start_iot_simulator():
            return False
        
        # Jalankan analisis data setelah beberapa menit
        def delayed_analysis():
            time.sleep(60)  # Tunggu 1 menit
            self.run_data_analysis()
        
        analysis_thread = threading.Thread(target=delayed_analysis, daemon=True)
        analysis_thread.start()
        
        # Monitor proses
        self.running = True
        monitor_thread = threading.Thread(target=self.monitor_processes, daemon=True)
        monitor_thread.start()
        
        print("\n" + "="*50)
        print("🎯 SISTEM BERJALAN!")
        print("="*50)
        print("📊 Dashboard: http://localhost:5000")
        print("🔌 API: http://localhost:5000/api")
        print("🌐 IoT Simulator: Berjalan di background")
        print("📈 Analisis Data: Akan dijalankan dalam 1 menit")
        print("\n🛑 Tekan Ctrl+C untuk menghentikan sistem")
        
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop_system()
    
    def stop_system(self):
        """Menghentikan seluruh sistem"""
        print("\n🛑 Menghentikan sistem...")
        self.running = False
        
        for name, process in self.processes.items():
            print(f"🛑 Menghentikan {name}...")
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
        
        print("✅ Sistem dihentikan!")

def main():
    """Main function"""
    runner = IoTSystemRunner()
    
    try:
        runner.start_system()
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        runner.stop_system()

if __name__ == "__main__":
    main() 