# 📊 Panduan MongoDB Compass untuk Sistem IoT

## 🚀 Setup MongoDB Compass

### 1. Download dan Install MongoDB Compass
1. Kunjungi: https://www.mongodb.com/try/download/compass
2. Download versi terbaru untuk Windows
3. Install dengan default settings
4. Buka MongoDB Compass

### 2. Connect ke Database
1. Buka MongoDB Compass
2. Di connection string, masukkan: `mongodb://localhost:27017`
3. Klik "Connect"
4. Pilih database `iot_monitoring`

## 📊 Struktur Database

### Database: `iot_monitoring`

#### Collection: `devices`
Berisi informasi perangkat IoT:
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
Berisi data time-series dari sensor:
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

## 🔍 Query Examples di MongoDB Compass

### 1. Lihat Semua Perangkat
```json
{}
```

### 2. Lihat Data Sensor Tertentu
```json
{
  "sensor_id": "temp001"
}
```

### 3. Lihat Data dalam Rentang Waktu
```json
{
  "timestamp": {
    "$gte": ISODate("2024-06-01T00:00:00Z"),
    "$lte": ISODate("2024-06-01T23:59:59Z")
  }
}
```

### 4. Lihat Data Perangkat Tertentu
```json
{
  "device_id": "dev001"
}
```

### 5. Lihat Data Sensor dengan Nilai Tertinggi
```json
{
  "sensor_type": "temperature"
}
```
Sort by: `value` (descending)

### 6. Lihat Data Terbaru
```json
{
  "sensor_id": "temp001"
}
```
Sort by: `timestamp` (descending)
Limit: 10

## 📈 Aggregation Pipeline Examples

### 1. Rata-rata Suhu per Jam
```json
[
  {
    "$match": {
      "sensor_type": "temperature"
    }
  },
  {
    "$group": {
      "_id": {
        "year": { "$year": "$timestamp" },
        "month": { "$month": "$timestamp" },
        "day": { "$dayOfMonth": "$timestamp" },
        "hour": { "$hour": "$timestamp" }
      },
      "avg_temp": { "$avg": "$value" },
      "min_temp": { "$min": "$value" },
      "max_temp": { "$max": "$value" },
      "count": { "$sum": 1 }
    }
  },
  {
    "$sort": { "_id": 1 }
  }
]
```

### 2. Statistik per Sensor
```json
[
  {
    "$group": {
      "_id": "$sensor_id",
      "avg_value": { "$avg": "$value" },
      "min_value": { "$min": "$value" },
      "max_value": { "$max": "$value" },
      "count": { "$sum": 1 }
    }
  }
]
```

### 3. Data Terbaru per Sensor
```json
[
  {
    "$sort": { "timestamp": -1 }
  },
  {
    "$group": {
      "_id": "$sensor_id",
      "latest": { "$first": "$$ROOT" }
    }
  }
]
```

## 🔧 Index Management

### 1. Buat Index untuk Query Time-Series
```javascript
db.sensor_readings.createIndex({
  "sensor_id": 1,
  "timestamp": -1
})
```

### 2. Buat Index untuk Query per Device
```javascript
db.sensor_readings.createIndex({
  "device_id": 1,
  "timestamp": -1
})
```

### 3. Buat Index untuk Query per Sensor Type
```javascript
db.sensor_readings.createIndex({
  "sensor_type": 1,
  "timestamp": -1
})
```

### 4. Buat TTL Index untuk Data Lama
```javascript
db.sensor_readings.createIndex(
  { "timestamp": 1 },
  { expireAfterSeconds: 7776000 } // 90 hari
)
```

## 📊 Visualisasi Data

### 1. Export Data untuk Analisis
1. Pilih collection `sensor_readings`
2. Klik "Export Collection"
3. Pilih format JSON atau CSV
4. Download file untuk analisis di Excel/Python

### 2. Real-time Monitoring
1. Buka collection `sensor_readings`
2. Klik "Schema" untuk melihat struktur data
3. Gunakan filter untuk melihat data real-time
4. Sort by `timestamp` descending untuk data terbaru

### 3. Data Analysis
1. Gunakan "Aggregations" tab
2. Buat pipeline untuk analisis data
3. Export hasil aggregation
4. Visualisasi dengan tools lain

## 🔍 Monitoring dan Maintenance

### 1. Cek Database Size
```javascript
db.stats()
```

### 2. Cek Collection Size
```javascript
db.sensor_readings.stats()
```

### 3. Cek Index Usage
```javascript
db.sensor_readings.getIndexes()
```

### 4. Optimize Database
```javascript
db.sensor_readings.reIndex()
```

## 🚨 Alert Monitoring

### 1. Cek Data Anomali (Suhu Tinggi)
```json
{
  "sensor_type": "temperature",
  "value": { "$gt": 30 }
}
```

### 2. Cek Data Anomali (Kelembapan Ekstrem)
```json
{
  "sensor_type": "humidity",
  "value": { "$or": [{ "$gt": 80 }, { "$lt": 30 }] }
}
```

### 3. Cek Data Anomali (CO2 Tinggi)
```json
{
  "sensor_type": "co2",
  "value": { "$gt": 1000 }
}
```

## 📱 Tips dan Trik

### 1. Real-time Monitoring
- Gunakan filter untuk melihat data terbaru
- Sort by timestamp descending
- Refresh secara berkala

### 2. Data Analysis
- Export data untuk analisis mendalam
- Gunakan aggregation pipeline untuk statistik
- Visualisasi dengan tools seperti Grafana

### 3. Performance
- Monitor index usage
- Optimize queries dengan proper indexing
- Implement TTL untuk data lama

### 4. Backup dan Recovery
- Export data secara berkala
- Backup database dengan mongodump
- Test restore procedure

## 🔗 Integrasi dengan Sistem

### 1. Dashboard Integration
- Data dari MongoDB Compass dapat diintegrasikan dengan dashboard
- Real-time updates melalui API
- Alert system berdasarkan threshold

### 2. API Integration
- MongoDB Compass dapat digunakan untuk debug API
- Verifikasi data yang masuk melalui API
- Monitor performance queries

### 3. Data Export
- Export data untuk analisis lanjutan
- Integrasi dengan tools analisis data
- Backup dan archival strategy 