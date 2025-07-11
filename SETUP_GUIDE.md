# 🚀 Panduan Setup Sistem Pemantauan IoT

## 📋 Prerequisites

### 1. Install Python
1. Download Python dari: https://www.python.org/downloads/
2. Pilih versi terbaru (3.8+)
3. **PENTING**: Centang "Add Python to PATH" saat instalasi
4. Restart terminal/command prompt setelah instalasi

### 2. Install MongoDB
1. Download MongoDB Community Server dari: https://www.mongodb.com/try/download/community
2. Install dengan default settings
3. Pastikan MongoDB service berjalan

### 3. Install MongoDB Compass
1. Download MongoDB Compass dari: https://www.mongodb.com/try/download/compass
2. Install dan buka MongoDB Compass
3. Connect ke: `mongodb://localhost:27017`

## 🔧 Setup Project

### Langkah 1: Cek Python
```bash
python --version
# Harus menampilkan versi Python (contoh: Python 3.9.7)
```

### Langkah 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Langkah 3: Cek MongoDB
```bash
python -c "from pymongo import MongoClient; client = MongoClient('mongodb://localhost:27017/'); print('MongoDB OK')"
```

### Langkah 4: Jalankan Sistem
```bash
python app.py
```

## 🌐 Akses Sistem

- **Dashboard**: http://localhost:5000
- **API**: http://localhost:5000/api
- **MongoDB Compass**: mongodb://localhost:27017

## 📊 Struktur Database di MongoDB Compass

### Database: `iot_monitoring`

#### Collection: `devices`
```json
{
  "_id": ObjectId("..."),
  "device_id": "dev001",
  "device_name": "Sensor Udara Ruang Lab",
  "location": "Ruang Lab",
  "description": "Sensor pemantauan kualitas udara",
  "sensors": [
    {
      "sensor_id": "temp001",
      "type": "temperature",
      "unit": "°C",
      "description": "Sensor suhu"
    }
  ]
}
```

#### Collection: `sensor_readings`
```json
{
  "_id": ObjectId("..."),
  "device_id": "dev001",
  "sensor_id": "temp001",
  "sensor_type": "temperature",
  "timestamp": ISODate("2024-06-01T10:00:00Z"),
  "value": 25.5,
  "unit": "°C"
}
```

## 🔍 Troubleshooting

### Error: Python not found
- Pastikan Python terinstall dan ada di PATH
- Restart terminal setelah install Python

### Error: MongoDB connection failed
- Pastikan MongoDB service berjalan
- Cek di Services (Windows) atau `sudo systemctl status mongod` (Linux)

### Error: Module not found
- Jalankan: `pip install -r requirements.txt`

### Error: Port 5000 already in use
- Ganti port di `app.py` atau matikan aplikasi yang menggunakan port 5000

## 🎯 Testing

### Test API
```bash
python test_api.py
```

### Test IoT Simulator
```bash
python iot_simulator.py
```

### Test Data Analysis
```bash
python data_analysis.py
```

## 📱 Fitur yang Tersedia

1. **Real-time Dashboard** - Monitor data sensor secara real-time
2. **IoT Simulator** - Simulasi perangkat IoT
3. **Data Analysis** - Analisis data sensor
4. **API Testing** - Test semua endpoint API
5. **MongoDB Compass** - Visualisasi database

## 🔄 Auto-refresh Dashboard

Dashboard akan auto-refresh setiap 30 detik untuk menampilkan data terbaru.

## 📈 Status Monitoring

- **Online**: Sistem berjalan normal
- **Offline**: Ada masalah koneksi atau sistem tidak berjalan
- **Warning**: Nilai sensor melebihi threshold
- **Danger**: Nilai sensor dalam kondisi berbahaya 