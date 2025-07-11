# Studi Kasus: Pengelolaan Data Time-Series dari Perangkat IoT Menggunakan NoSQL Database pada Sistem Pemantauan Lingkungan

## 1. Analisis Kebutuhan

### 1.1 Kebutuhan Fungsional

#### a) Pengumpulan Data Sensor
- Sistem harus mampu menerima data dari berbagai perangkat IoT secara real-time
- Mendukung multiple tipe sensor: suhu, kelembapan, CO2, dan parameter lingkungan lainnya
- Data harus disimpan dengan timestamp yang akurat
- Sistem harus dapat menangani data dari multiple lokasi perangkat

#### b) Penyimpanan Data Time-Series
- Data sensor harus disimpan dalam format time-series yang efisien
- Mendukung query berdasarkan rentang waktu
- Optimasi untuk read-heavy dan write-heavy operations
- Implementasi TTL (Time To Live) untuk data lama

#### c) Query dan Analisis Data
- Query data berdasarkan rentang waktu tertentu
- Query data berdasarkan tipe sensor atau lokasi perangkat
- Analisis tren data sensor
- Deteksi anomali dan outlier
- Generate laporan statistik

#### d) Visualisasi dan Monitoring
- Dashboard real-time untuk monitoring data sensor
- Grafik tren data sensor
- Alert system berdasarkan threshold nilai
- Status monitoring perangkat IoT

#### e) Manajemen Perangkat
- Registrasi perangkat IoT baru
- Monitoring status perangkat
- Konfigurasi sensor per perangkat
- Manajemen lokasi perangkat

### 1.2 Kebutuhan Non-Fungsional

#### a) Skalabilitas
- Sistem harus mampu menangani pertambahan perangkat IoT
- Volume data yang besar (ribuan pembacaan per jam)
- Horizontal scaling untuk database
- Load balancing untuk API

#### b) Ketersediaan Tinggi
- Sistem harus tetap berjalan meski ada sebagian node yang gagal
- Redundancy untuk database
- Auto-recovery dari kegagalan
- Monitoring kesehatan sistem

#### c) Konsistensi Data
- Data yang disimpan harus akurat dan tidak duplikat
- Atomic operations untuk write operations
- Eventual consistency untuk read operations
- Data validation dan sanitization

#### d) Keamanan
- Autentikasi untuk akses API
- Enkripsi data sensitif
- Rate limiting untuk mencegah abuse
- Audit trail untuk aktivitas sistem

#### e) Responsivitas
- Query data harus cepat, terutama untuk data terbaru
- Real-time dashboard updates
- Optimasi untuk time-series queries
- Caching untuk data yang sering diakses

### 1.3 Jenis Data dan Hubungannya

#### a) Perangkat (Device)
```json
{
  "device_id": "dev001",
  "device_name": "Sensor Udara Ruang Lab",
  "location": "Ruang Lab",
  "description": "Sensor pemantauan kualitas udara",
  "status": "active",
  "created_at": "2024-06-01T10:00:00Z"
}
```

#### b) Sensor
```json
{
  "sensor_id": "temp001",
  "device_id": "dev001",
  "type": "temperature",
  "unit": "°C",
  "description": "Sensor suhu",
  "calibration_date": "2024-06-01T10:00:00Z"
}
```

#### c) Data Sensor (Time-Series)
```json
{
  "device_id": "dev001",
  "sensor_id": "temp001",
  "sensor_type": "temperature",
  "timestamp": "2024-06-01T10:00:00Z",
  "value": 25.5,
  "unit": "°C",
  "quality": "good"
}
```

#### d) Pengguna
```json
{
  "user_id": "user001",
  "username": "admin",
  "email": "admin@example.com",
  "role": "admin",
  "permissions": ["read", "write", "admin"]
}
```

**Relasi Data:**
- Satu perangkat memiliki banyak sensor (1:N)
- Satu sensor menghasilkan banyak data time-series (1:N)
- Pengguna dapat mengakses data dari beberapa perangkat (M:N)

## 2. Pemilihan & Justifikasi Database NoSQL

### 2.1 Pilihan Database NoSQL

#### a) MongoDB (Document Database)
**Karakteristik:**
- Schema-less document storage
- JSON-like document structure
- Rich query language dengan aggregation framework
- Support untuk indexing yang fleksibel
- Built-in support untuk time-series data

**Alasan Pemilihan:**
1. **Fleksibilitas Schema**: Mudah menambah field baru tanpa mengubah struktur
2. **Query Kompleks**: Aggregation pipeline untuk analisis data yang kompleks
3. **Time-Series Support**: TTL indexes dan optimasi untuk data time-series
4. **Horizontal Scaling**: Sharding untuk distribusi data
5. **JSON Native**: Mudah integrasi dengan aplikasi web

#### b) Cassandra (Wide-Column Database)
**Karakteristik:**
- Distributed database dengan linear scalability
- Optimized untuk write-heavy workloads
- Tunable consistency levels
- Excellent untuk time-series data
- High availability dengan multi-datacenter support

**Alasan Pemilihan:**
1. **Time-Series Optimization**: Sangat baik untuk data time-series dengan volume besar
2. **Write Performance**: Sangat cepat untuk write operations
3. **Linear Scalability**: Skalabilitas linear dengan penambahan node
4. **High Availability**: Tahan terhadap kegagalan node
5. **Multi-Datacenter**: Support untuk deployment geografis

### 2.2 Perbandingan Keunggulan & Kelemahan

| Aspek | MongoDB | Cassandra |
|-------|---------|-----------|
| **Skema Data** | Fleksibel, schema-less | Fleksibel, tapi lebih rigid |
| **Query Language** | Rich query dengan aggregation | CQL (SQL-like), terbatas |
| **Time-Series** | Baik, dengan TTL support | Sangat optimal |
| **Write Performance** | Baik | Sangat baik |
| **Read Performance** | Sangat baik untuk query kompleks | Baik untuk query sederhana |
| **Skalabilitas** | Horizontal dengan sharding | Linear scalability |
| **Konsistensi** | Strong consistency per document | Tunable consistency |
| **Ketersediaan** | High dengan replica sets | Sangat tinggi |
| **Learning Curve** | Mudah | Sedang-tinggi |
| **Community** | Sangat besar | Besar |

### 2.3 Justifikasi untuk Studi Kasus IoT

**MongoDB dipilih sebagai database utama karena:**

1. **Fleksibilitas Data IoT**: Data IoT sering berubah struktur dan MongoDB mendukung schema evolution
2. **Query Kompleks**: Perlu analisis data yang kompleks (aggregation, grouping, filtering)
3. **JSON Native**: Mudah integrasi dengan REST API dan frontend
4. **Time-Series Support**: Built-in TTL dan indexing untuk data time-series
5. **Development Speed**: Lebih cepat untuk development dan prototyping

**Cassandra sebagai alternatif untuk skala besar:**
- Jika volume data sangat besar (>1M readings/hour)
- Jika write performance menjadi bottleneck
- Jika perlu multi-datacenter deployment

## 3. Desain Model Data

### 3.1 MongoDB Model Data

#### Collection: `devices`
```json
{
  "_id": ObjectId("..."),
  "device_id": "dev001",
  "device_name": "Sensor Udara Ruang Lab",
  "location": "Ruang Lab",
  "description": "Sensor pemantauan kualitas udara di ruang laboratorium",
  "status": "active",
  "created_at": ISODate("2024-06-01T10:00:00Z"),
  "updated_at": ISODate("2024-06-01T10:00:00Z"),
  "sensors": [
    {
      "sensor_id": "temp001",
      "type": "temperature",
      "unit": "°C",
      "description": "Sensor suhu",
      "calibration_date": ISODate("2024-06-01T10:00:00Z")
    },
    {
      "sensor_id": "hum001",
      "type": "humidity",
      "unit": "%",
      "description": "Sensor kelembapan",
      "calibration_date": ISODate("2024-06-01T10:00:00Z")
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
  "unit": "°C",
  "quality": "good",
  "metadata": {
    "battery_level": 85,
    "signal_strength": -45
  }
}
```

### 3.2 Cassandra Model Data

#### Table: `sensor_readings`
```sql
CREATE TABLE sensor_readings (
    device_id text,
    sensor_id text,
    timestamp timestamp,
    value double,
    unit text,
    quality text,
    PRIMARY KEY ((device_id, sensor_id), timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC);
```

#### Table: `devices`
```sql
CREATE TABLE devices (
    device_id text PRIMARY KEY,
    device_name text,
    location text,
    description text,
    status text,
    created_at timestamp
);
```

### 3.3 Optimasi Model Data

#### a) Indexing Strategy
```javascript
// MongoDB Indexes
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

// TTL Index untuk data lama
db.sensor_readings.createIndex(
    { "timestamp": 1 },
    { expireAfterSeconds: 7776000 } // 90 hari
)
```

#### b) Denormalisasi
- Data sensor di-embed dalam device document untuk query cepat
- Metadata device disimpan di setiap reading untuk analisis
- Unit dan tipe sensor disimpan di setiap reading untuk efisiensi

#### c) Sharding Strategy
- Shard berdasarkan `device_id` untuk distribusi yang merata
- Time-based sharding untuk data historis
- Sensor-type sharding untuk analisis per tipe sensor

## 4. Implementasi Prototype

### 4.1 Arsitektur Sistem
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

### 4.2 Komponen Implementasi

#### a) Backend API (Flask)
- RESTful API untuk semua operasi CRUD
- Real-time data processing
- Data validation dan sanitization
- Error handling dan logging

#### b) Database Layer (MongoDB)
- Connection pooling
- Optimized queries untuk time-series data
- Indexing strategy
- Data aggregation

#### c) Frontend Dashboard
- Real-time monitoring interface
- Interactive charts dan graphs
- Alert system
- Device management interface

#### d) IoT Simulator
- Simulasi perangkat IoT
- Data generation yang realistis
- Multiple sensor types
- Configurable intervals

### 4.3 Query Implementasi

#### 1. Query Data Sensor dalam Rentang Waktu
```python
def get_sensor_readings(sensor_id, start_time, end_time):
    query = {
        "sensor_id": sensor_id,
        "timestamp": {
            "$gte": start_time,
            "$lte": end_time
        }
    }
    return db.sensor_readings.find(query).sort("timestamp", -1)
```

#### 2. Query Data Perangkat
```python
def get_device_readings(device_id, limit=100):
    query = {"device_id": device_id}
    return db.sensor_readings.find(query).sort("timestamp", -1).limit(limit)
```

#### 3. Query Statistik Sensor
```python
def get_sensor_stats(sensor_id):
    pipeline = [
        {"$match": {"sensor_id": sensor_id}},
        {"$group": {
            "_id": None,
            "avg_value": {"$avg": "$value"},
            "min_value": {"$min": "$value"},
            "max_value": {"$max": "$value"},
            "count": {"$sum": 1}
        }}
    ]
    return db.sensor_readings.aggregate(pipeline)
```

#### 4. Query Anomali Detection
```python
def detect_anomalies(sensor_id, threshold=2.0):
    pipeline = [
        {"$match": {"sensor_id": sensor_id}},
        {"$group": {
            "_id": None,
            "avg": {"$avg": "$value"},
            "std": {"$stdDevPop": "$value"}
        }},
        {"$project": {
            "anomalies": {
                "$filter": {
                    "input": "$readings",
                    "cond": {
                        "$gt": [
                            {"$abs": {"$subtract": ["$$this.value", "$avg"]}},
                            {"$multiply": ["$std", threshold]}
                        ]
                    }
                }
            }
        }}
    ]
    return db.sensor_readings.aggregate(pipeline)
```

#### 5. Query Real-time Monitoring
```python
def get_latest_readings(device_id):
    pipeline = [
        {"$match": {"device_id": device_id}},
        {"$sort": {"timestamp": -1}},
        {"$group": {
            "_id": "$sensor_id",
            "latest": {"$first": "$$ROOT"}
        }}
    ]
    return db.sensor_readings.aggregate(pipeline)
```

## 5. Evaluasi & Kesimpulan

### 5.1 Tantangan yang Dihadapi

#### a) Desain Skema Data
- **Tantangan**: Menentukan struktur data yang optimal untuk query dan penyimpanan
- **Solusi**: Implementasi denormalisasi yang tepat dan indexing strategy yang optimal

#### b) Manajemen Data Time-Series
- **Tantangan**: Volume data besar dan kebutuhan query yang cepat
- **Solusi**: Implementasi TTL, indexing, dan sharding strategy

#### c) Query Performance
- **Tantangan**: Query kompleks untuk analisis data
- **Solusi**: Aggregation pipeline optimization dan proper indexing

#### d) Real-time Processing
- **Tantangan**: Menangani data real-time dari multiple devices
- **Solusi**: Asynchronous processing dan connection pooling

### 5.2 Kesesuaian Database NoSQL

#### MongoDB untuk Studi Kasus IoT:
**✅ Keunggulan:**
- Fleksibilitas schema sangat cocok untuk data IoT yang beragam
- Aggregation framework powerful untuk analisis data
- JSON native memudahkan integrasi dengan web APIs
- TTL support optimal untuk data time-series
- Community support yang besar

**⚠️ Kelemahan:**
- Write performance tidak seoptimal Cassandra untuk volume sangat besar
- Memory usage tinggi untuk data besar
- Consistency model mungkin terlalu strict untuk beberapa use case

#### Cassandra untuk Studi Kasus IoT:
**✅ Keunggulan:**
- Write performance sangat baik untuk volume besar
- Linear scalability yang excellent
- Built-in support untuk time-series data
- High availability dengan multi-datacenter

**⚠️ Kelemahan:**
- Query complexity terbatas
- Learning curve lebih tinggi
- Schema design lebih rigid

### 5.3 Kesimpulan

**MongoDB adalah pilihan terbaik untuk studi kasus ini karena:**

1. **Fleksibilitas**: Data IoT sering berubah struktur dan MongoDB mendukung schema evolution
2. **Query Power**: Aggregation framework sangat powerful untuk analisis data IoT
3. **Development Speed**: Lebih cepat untuk development dan prototyping
4. **Time-Series Support**: Built-in TTL dan indexing untuk data time-series
5. **JSON Native**: Mudah integrasi dengan REST API dan frontend

**Rekomendasi untuk Production:**
- Gunakan MongoDB untuk development dan skala menengah
- Pertimbangkan Cassandra jika volume data > 1M readings/hour
- Implementasi caching layer (Redis) untuk data yang sering diakses
- Monitoring dan alerting untuk database performance

### 5.4 Saran Pengembangan Lanjutan

#### a) Skalabilitas
- Implementasi horizontal scaling dengan sharding
- Load balancing untuk API layer
- Caching strategy dengan Redis
- Microservices architecture

#### b) Keamanan
- Implementasi JWT authentication
- Role-based access control (RBAC)
- Data encryption at rest
- API rate limiting

#### c) Monitoring & Analytics
- Real-time dashboard dengan Grafana
- Machine learning untuk predictive maintenance
- Advanced anomaly detection
- Automated alerting system

#### d) Data Management
- Data archival strategy
- Backup dan recovery procedures
- Data retention policies
- Compliance dengan regulasi

---

**Implementasi lengkap dapat dilihat di file-file project yang telah dibuat:**
- `app.py` - Flask API backend
- `templates/dashboard.html` - Web dashboard
- `iot_simulator.py` - IoT device simulator
- `data_analysis.py` - Data analysis tools
- `test_api.py` - API testing
- `run_system.py` - System runner 