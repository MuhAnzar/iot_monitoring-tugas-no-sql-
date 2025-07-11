<<<<<<< HEAD
# Sistem Pemantauan Lingkungan IoT dengan MongoDB

## 📋 Deskripsi

Sistem pemantauan lingkungan IoT yang menggunakan MongoDB sebagai database NoSQL untuk menyimpan dan mengelola data time-series dari perangkat sensor IoT. Sistem ini dirancang untuk memantau kualitas udara, suhu, kelembapan, dan parameter lingkungan lainnya secara real-time.

> **Catatan:** Koneksi ke MongoDB dilakukan otomatis oleh aplikasi. Anda **tidak perlu menjalankan mongo shell** secara manual. Pastikan service MongoDB sudah berjalan di komputer Anda. Jika MongoDB tidak aktif, aplikasi akan otomatis menggunakan data in-memory (data tidak akan tersimpan permanen).

## 🏗️ Arsitektur Sistem

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   IoT Devices   │───▶│   Flask API     │───▶│   MongoDB       │
│   (Sensors)     │    │   (Backend)     │    │   (Database)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Web Dashboard │
                       │   (Frontend)    │
                       └─────────────────┘
```

## 🚀 Fitur Utama

- **Real-time Monitoring**: Dashboard real-time untuk memantau data sensor
- **Time-series Data**: Penyimpanan dan query data time-series yang efisien
- **Multi-device Support**: Mendukung multiple perangkat IoT
- **RESTful API**: API lengkap untuk integrasi dengan sistem lain
- **Visualisasi Data**: Grafik interaktif untuk analisis tren
- **Alert System**: Sistem peringatan berdasarkan threshold nilai sensor
- **Export CSV**: Ekspor data pembacaan sensor perangkat ke file CSV langsung dari dashboard
- **Auto Sample Data**: Data sample otomatis di-generate saat pertama kali dijalankan
- **Fallback In-Memory**: Jika MongoDB tidak aktif, aplikasi tetap berjalan dengan data sementara (tidak permanen)

## 📊 Model Data

### Collection: `devices`
```json
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
    }
  ]
}
```

### Collection: `sensor_readings`
```json
{
  "device_id": "dev001",
  "sensor_id": "temp001",
  "sensor_type": "temperature",
  "timestamp": "2024-06-01T10:00:00Z",
  "value": 25.5,
  "unit": "°C"
}
```

## 🛠️ Instalasi & Setup

### Prasyarat
- Python 3.8+
- MongoDB 4.4+ (pastikan service berjalan, tidak perlu buka mongo shell)
- pip (Python package manager)

### Langkah Instalasi

1. **Clone repository**
```bash
git clone <repository-url>
cd nosql
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Setup MongoDB**
   - Pastikan MongoDB berjalan di `localhost:27017`
   - Atau set environment variable `MONGO_URI` untuk koneksi custom
   - **Tidak perlu menjalankan mongo shell, cukup pastikan servicenya aktif**

4. **Jalankan aplikasi**
```bash
python app.py
```

5. **Akses dashboard**
   - Buka browser ke `http://localhost:5000`
   - Dashboard akan otomatis memuat data sample

6. **Cek data secara manual (opsional)**
   - Anda dapat menggunakan **MongoDB Compass** untuk melihat data di database secara visual.
   - Lihat panduan di file `MONGODB_COMPASS_GUIDE.md`.

## 📚 API Documentation

### Base URL
```
http://localhost:5000/api
```

### Endpoints

#### 1. GET `/devices`
Mendapatkan semua perangkat IoT.

#### 2. GET `/devices/{device_id}`
Mendapatkan perangkat spesifik berdasarkan ID.

#### 3. GET `/sensors/{sensor_id}/readings`
Mendapatkan pembacaan sensor dengan parameter:
- `start_time`: Waktu mulai (ISO format)
- `end_time`: Waktu selesai (ISO format)
- `limit`: Jumlah maksimal data (default: 100)

#### 4. GET `/devices/{device_id}/readings`
Mendapatkan semua pembacaan dari perangkat tertentu.

#### 5. GET `/sensors/{sensor_id}/latest`
Mendapatkan pembacaan terbaru dari sensor tertentu.

#### 6. POST `/readings`
Menambah pembacaan sensor baru.

#### 7. POST `/devices`
Menambah perangkat IoT baru.

#### 8. GET `/stats`
Mendapatkan statistik sistem.

#### 9. GET `/devices/{device_id}/readings/export`
Export seluruh pembacaan sensor dari perangkat tertentu dalam format CSV.

## 📈 Dashboard Features

- **Real-time Monitoring**: Tampilan nilai sensor real-time, auto-refresh setiap 30 detik
- **Data Visualization**: Grafik line chart untuk tren sensor, pemilihan sensor untuk visualisasi
- **Device Management**: Daftar semua perangkat IoT, info lokasi & sensor
- **Alert System**: Peringatan otomatis berdasarkan threshold (lihat konfigurasi di bawah)
- **Export CSV Data**: Tombol Export CSV di dashboard
- **Tampilan Perangkat & Sensor**: Maksimal 2 perangkat ditampilkan di dashboard

## 🔧 Konfigurasi

### Environment Variables
```bash
MONGO_URI=mongodb://localhost:27017/
FLASK_ENV=development
```

### Threshold Values
Threshold untuk alert system dapat dikonfigurasi di `app.py`:

```python
# Temperature thresholds
TEMP_DANGER = 30
TEMP_WARNING = 25

# Humidity thresholds
HUMIDITY_DANGER_HIGH = 80
HUMIDITY_DANGER_LOW = 30
HUMIDITY_WARNING_HIGH = 70
HUMIDITY_WARNING_LOW = 40

# CO2 thresholds
CO2_DANGER = 1000
CO2_WARNING = 800
```

## 📊 Optimasi Database

### Indexing Strategy
```javascript
// Index untuk query time-series
db.sensor_readings.createIndex({
  "sensor_id": 1,
  "timestamp": -1
})

db.sensor_readings.createIndex({
  "device_id": 1,
  "timestamp": -1
})

db.sensor_readings.createIndex({
  "sensor_type": 1,
  "timestamp": -1
})
```

### TTL (Time To Live)
Untuk data lama, dapat diimplementasikan TTL:
```javascript
db.sensor_readings.createIndex(
  { "timestamp": 1 },
  { expireAfterSeconds: 7776000 } // 90 hari
)
```

## 🚀 Deployment

### Production Setup
1. **Environment Variables**
```bash
export FLASK_ENV=production
export MONGO_URI=mongodb://your-mongo-host:27017/
```

2. **WSGI Server**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

3. **Reverse Proxy (Nginx)**
```nginx
server {
    listen 80;
    server_name your-domain.com;
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🔒 Security Considerations

1. **Authentication**: Implementasi JWT untuk API access
2. **Rate Limiting**: Batasi request per IP
3. **Input Validation**: Validasi semua input data
4. **HTTPS**: Gunakan SSL/TLS untuk production
5. **MongoDB Security**: Enable authentication dan authorization

## 📈 Monitoring & Logging

### Logging Configuration
```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Health Check Endpoint
```python
@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "connected"
    })
```


