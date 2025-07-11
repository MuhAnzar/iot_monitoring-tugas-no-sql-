# API Documentation - Sistem Pemantauan Lingkungan IoT

## Base URL
```
http://localhost:5000/api
```

## Authentication
Saat ini API tidak memerlukan authentication. Untuk production, implementasi JWT authentication direkomendasikan.

## Response Format
Semua response menggunakan format JSON dengan struktur:
```json
{
  "success": true,
  "data": {...},
  "message": "Success message"
}
```

## Error Response Format
```json
{
  "success": false,
  "error": "Error message",
  "code": 400
}
```

---

## Endpoints

### 1. Devices Management

#### GET `/devices`
Mendapatkan semua perangkat IoT.

**Response:**
```json
[
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
      }
    ]
  }
]
```

#### GET `/devices/{device_id}`
Mendapatkan perangkat spesifik berdasarkan ID.

**Parameters:**
- `device_id` (string): ID perangkat

**Response:**
```json
{
  "device_id": "dev001",
  "device_name": "Sensor Udara Ruang Lab",
  "location": "Ruang Lab",
  "description": "Sensor pemantauan kualitas udara di ruang laboratorium",
  "sensors": [...]
}
```

#### POST `/devices`
Menambah perangkat IoT baru.

**Request Body:**
```json
{
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
    }
  ]
}
```

**Response:**
```json
{
  "device_id": "dev003",
  "device_name": "Sensor Udara Ruang Meeting",
  "location": "Ruang Meeting",
  "description": "Sensor pemantauan kualitas udara di ruang meeting",
  "sensors": [...]
}
```

### 2. Sensor Readings

#### GET `/sensors/{sensor_id}/readings`
Mendapatkan pembacaan sensor dengan filter.

**Parameters:**
- `sensor_id` (string): ID sensor
- `start_time` (string, optional): Waktu mulai (ISO format)
- `end_time` (string, optional): Waktu selesai (ISO format)
- `limit` (integer, optional): Jumlah maksimal data (default: 100)

**Example:**
```
GET /api/sensors/temp001/readings?start_time=2024-06-01T10:00:00Z&limit=50
```

**Response:**
```json
[
  {
    "device_id": "dev001",
    "sensor_id": "temp001",
    "sensor_type": "temperature",
    "timestamp": "2024-06-01T10:00:00Z",
    "value": 25.5,
    "unit": "°C"
  }
]
```

#### GET `/sensors/{sensor_id}/latest`
Mendapatkan pembacaan terbaru dari sensor.

**Parameters:**
- `sensor_id` (string): ID sensor

**Response:**
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

#### POST `/readings`
Menambah pembacaan sensor baru.

**Request Body:**
```json
{
  "device_id": "dev001",
  "sensor_id": "temp001",
  "sensor_type": "temperature",
  "value": 25.5,
  "unit": "°C"
}
```

**Response:**
```json
{
  "device_id": "dev001",
  "sensor_id": "temp001",
  "sensor_type": "temperature",
  "timestamp": "2024-06-01T10:00:00Z",
  "value": 25.5,
  "unit": "°C",
  "_id": "507f1f77bcf86cd799439011"
}
```

### 3. Device Readings

#### GET `/devices/{device_id}/readings`
Mendapatkan semua pembacaan dari perangkat tertentu.

**Parameters:**
- `device_id` (string): ID perangkat
- `start_time` (string, optional): Waktu mulai (ISO format)
- `end_time` (string, optional): Waktu selesai (ISO format)
- `limit` (integer, optional): Jumlah maksimal data (default: 100)

**Example:**
```
GET /api/devices/dev001/readings?limit=50
```

**Response:**
```json
[
  {
    "device_id": "dev001",
    "sensor_id": "temp001",
    "sensor_type": "temperature",
    "timestamp": "2024-06-01T10:00:00Z",
    "value": 25.5,
    "unit": "°C"
  },
  {
    "device_id": "dev001",
    "sensor_id": "hum001",
    "sensor_type": "humidity",
    "timestamp": "2024-06-01T10:00:00Z",
    "value": 60.0,
    "unit": "%"
  }
]
```

### 4. System Statistics

#### GET `/stats`
Mendapatkan statistik sistem.

**Response:**
```json
{
  "total_devices": 2,
  "total_readings": 1440,
  "latest_readings": {
    "temperature": {
      "device_id": "dev001",
      "sensor_id": "temp001",
      "sensor_type": "temperature",
      "timestamp": "2024-06-01T10:00:00Z",
      "value": 25.5,
      "unit": "°C"
    },
    "humidity": {
      "device_id": "dev001",
      "sensor_id": "hum001",
      "sensor_type": "humidity",
      "timestamp": "2024-06-01T10:00:00Z",
      "value": 60.0,
      "unit": "%"
    }
  }
}
```

---

## Query Examples

### 1. Mendapatkan Data Sensor dalam Rentang Waktu
```bash
curl "http://localhost:5000/api/sensors/temp001/readings?start_time=2024-06-01T00:00:00Z&end_time=2024-06-01T23:59:59Z&limit=100"
```

### 2. Menambah Pembacaan Sensor
```bash
curl -X POST "http://localhost:5000/api/readings" \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "dev001",
    "sensor_id": "temp001",
    "sensor_type": "temperature",
    "value": 26.5,
    "unit": "°C"
  }'
```

### 3. Mendapatkan Statistik Sistem
```bash
curl "http://localhost:5000/api/stats"
```

### 4. Menambah Perangkat Baru
```bash
curl -X POST "http://localhost:5000/api/devices" \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "dev004",
    "device_name": "Sensor Udara Ruang Konferensi",
    "location": "Ruang Konferensi",
    "description": "Sensor pemantauan kualitas udara di ruang konferensi",
    "sensors": [
      {
        "sensor_id": "temp004",
        "type": "temperature",
        "unit": "°C",
        "description": "Sensor suhu"
      },
      {
        "sensor_id": "hum004",
        "type": "humidity",
        "unit": "%",
        "description": "Sensor kelembapan"
      }
    ]
  }'
```

---

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request - Invalid input data |
| 404 | Not Found - Resource tidak ditemukan |
| 409 | Conflict - Resource sudah ada |
| 500 | Internal Server Error |

---

## Rate Limiting
Saat ini tidak ada rate limiting. Untuk production, implementasi rate limiting direkomendasikan:
- 100 requests per minute untuk GET endpoints
- 50 requests per minute untuk POST endpoints

---

## Data Validation

### Sensor Reading Validation
- `device_id`: Required, string
- `sensor_id`: Required, string
- `sensor_type`: Required, string (temperature, humidity, co2, etc.)
- `value`: Required, numeric
- `unit`: Required, string

### Device Validation
- `device_id`: Required, string, unique
- `device_name`: Required, string
- `location`: Optional, string
- `description`: Optional, string
- `sensors`: Optional, array of sensor objects

---

## WebSocket Support (Future)
Untuk real-time updates, WebSocket endpoint dapat diimplementasikan:
```
ws://localhost:5000/ws/sensors
```

---

## SDK Examples

### Python SDK
```python
import requests

class IoTApiClient:
    def __init__(self, base_url="http://localhost:5000/api"):
        self.base_url = base_url
    
    def get_devices(self):
        response = requests.get(f"{self.base_url}/devices")
        return response.json()
    
    def add_reading(self, device_id, sensor_id, sensor_type, value, unit):
        data = {
            "device_id": device_id,
            "sensor_id": sensor_id,
            "sensor_type": sensor_type,
            "value": value,
            "unit": unit
        }
        response = requests.post(f"{self.base_url}/readings", json=data)
        return response.json()
    
    def get_sensor_readings(self, sensor_id, start_time=None, end_time=None, limit=100):
        params = {"limit": limit}
        if start_time:
            params["start_time"] = start_time
        if end_time:
            params["end_time"] = end_time
        
        response = requests.get(f"{self.base_url}/sensors/{sensor_id}/readings", params=params)
        return response.json()

# Usage
client = IoTApiClient()
devices = client.get_devices()
readings = client.get_sensor_readings("temp001", limit=50)
```

### JavaScript SDK
```javascript
class IoTApiClient {
    constructor(baseUrl = 'http://localhost:5000/api') {
        this.baseUrl = baseUrl;
    }
    
    async getDevices() {
        const response = await fetch(`${this.baseUrl}/devices`);
        return await response.json();
    }
    
    async addReading(deviceId, sensorId, sensorType, value, unit) {
        const data = {
            device_id: deviceId,
            sensor_id: sensorId,
            sensor_type: sensorType,
            value: value,
            unit: unit
        };
        
        const response = await fetch(`${this.baseUrl}/readings`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        return await response.json();
    }
    
    async getSensorReadings(sensorId, options = {}) {
        const params = new URLSearchParams({
            limit: options.limit || 100,
            ...(options.startTime && { start_time: options.startTime }),
            ...(options.endTime && { end_time: options.endTime })
        });
        
        const response = await fetch(`${this.baseUrl}/sensors/${sensorId}/readings?${params}`);
        return await response.json();
    }
}

// Usage
const client = new IoTApiClient();
const devices = await client.getDevices();
const readings = await client.getSensorReadings('temp001', { limit: 50 });
```

---

## Testing

Gunakan script `test_api.py` untuk testing semua endpoints:

```bash
python test_api.py
```

Atau test manual dengan curl:

```bash
# Test get devices
curl http://localhost:5000/api/devices

# Test get sensor readings
curl http://localhost:5000/api/sensors/temp001/readings?limit=5

# Test add reading
curl -X POST http://localhost:5000/api/readings \
  -H "Content-Type: application/json" \
  -d '{"device_id":"dev001","sensor_id":"temp001","sensor_type":"temperature","value":25.5,"unit":"°C"}'
``` 