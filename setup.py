#!/usr/bin/env python3
"""
Script Setup Otomatis untuk Sistem Pemantauan IoT
"""

import sys
import subprocess
import os
import platform

def print_header():
    """Print header aplikasi"""
    print("🌐 SISTEM PEMANTAUAN LINGKUNGAN IoT")
    print("=" * 50)
    print("Setup dan Konfigurasi Otomatis")
    print("=" * 50)

def check_python():
    """Cek apakah Python tersedia"""
    print("🔍 Memeriksa Python...")
    try:
        version = sys.version_info
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} terdeteksi")
        return True
    except Exception as e:
        print(f"❌ Python tidak terdeteksi: {e}")
        return False

def install_dependencies():
    """Install dependencies"""
    print("\n📦 Menginstall dependencies...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Dependencies berhasil diinstall")
            return True
        else:
            print(f"❌ Error menginstall dependencies: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_mongodb():
    """Cek koneksi MongoDB"""
    print("\n🔍 Memeriksa MongoDB...")
    try:
        from pymongo import MongoClient
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=3000)
        client.server_info()
        print("✅ MongoDB terhubung!")
        return True
    except Exception as e:
        print(f"⚠️  MongoDB tidak terhubung: {e}")
        print("\n💡 Untuk menggunakan MongoDB Compass:")
        print("1. Download MongoDB dari: https://www.mongodb.com/try/download/community")
        print("2. Download MongoDB Compass dari: https://www.mongodb.com/try/download/compass")
        print("3. Install dan jalankan MongoDB service")
        print("4. Connect Compass ke: mongodb://localhost:27017")
        return False

def create_sample_data():
    """Buat sample data jika MongoDB tersedia"""
    print("\n📊 Membuat sample data...")
    try:
        from app import init_database
        init_database()
        print("✅ Sample data berhasil dibuat")
        return True
    except Exception as e:
        print(f"⚠️  Tidak dapat membuat sample data: {e}")
        return False

def start_system():
    """Jalankan sistem"""
    print("\n🚀 Menjalankan sistem...")
    print("📊 Dashboard akan tersedia di: http://localhost:5000")
    print("🔌 API tersedia di: http://localhost:5000/api")
    print("\n🛑 Tekan Ctrl+C untuk menghentikan sistem")
    
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n✅ Sistem dihentikan")
    except Exception as e:
        print(f"❌ Error menjalankan sistem: {e}")

def show_instructions():
    """Tampilkan instruksi manual"""
    print("\n📋 INSTRUKSI MANUAL:")
    print("=" * 50)
    print("1. Install Python dari: https://www.python.org/downloads/")
    print("2. Install MongoDB dari: https://www.mongodb.com/try/download/community")
    print("3. Install MongoDB Compass dari: https://www.mongodb.com/try/download/compass")
    print("4. Jalankan MongoDB service")
    print("5. Buka terminal di folder project ini")
    print("6. Jalankan: python setup.py")
    print("\n📱 Setelah sistem berjalan:")
    print("- Dashboard: http://localhost:5000")
    print("- API: http://localhost:5000/api")
    print("- MongoDB Compass: mongodb://localhost:27017")

def main():
    """Main function"""
    print_header()
    
    # Cek Python
    if not check_python():
        print("\n❌ Python tidak tersedia!")
        show_instructions()
        return
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Gagal menginstall dependencies!")
        return
    
    # Cek MongoDB
    mongodb_ok = check_mongodb()
    
    # Buat sample data jika MongoDB tersedia
    if mongodb_ok:
        create_sample_data()
    
    # Tanya user apakah ingin menjalankan sistem
    print("\n🎯 Apakah Anda ingin menjalankan sistem sekarang?")
    print("1. Ya, jalankan sistem")
    print("2. Tidak, saya akan menjalankan manual")
    
    try:
        choice = input("Pilih (1/2): ").strip()
        if choice == "1":
            start_system()
        else:
            print("\n💡 Untuk menjalankan sistem manual:")
            print("python app.py")
    except KeyboardInterrupt:
        print("\n✅ Setup selesai")

if __name__ == "__main__":
    main() 