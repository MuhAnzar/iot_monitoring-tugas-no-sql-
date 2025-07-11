function displayDevices(devices) {
    const container = document.getElementById('devicesContainer');
    let html = '';
    devices.slice(0, 2).forEach(device => {
        html += `
            <div class="sensor-card p-3 mb-3">
                <div class="row align-items-center">
                    <div class="col-md-4">
                        <h6 class="mb-1"><i class="fas fa-microchip"></i> ${device.device_name}</h6>
                        <small class="text-light"><i class="fas fa-map-marker-alt"></i> ${device.location}</small>
                    </div>
                    <div class="col-md-8">
                        <div class="row">
        `;
        device.sensors.forEach(sensor => {
            html += `
                <div class="col-md-4 mb-2">
                    <div class="text-center">
                        <div class="sensor-value" id="sensor-${sensor.sensor_id}">-</div>
                        <div class="sensor-unit">${sensor.type} (${sensor.unit})</div>
                        <small>${sensor.description}</small>
                    </div>
                </div>
            `;
        });
        html += `
                        </div>
                    </div>
                </div>
            </div>
        `;
    });
    container.innerHTML = html;
    updateSensorValues();
}
async function updateSensorValues() {
    try {
        const devicesResponse = await fetch('/api/devices');
        const devices = await devicesResponse.json();
        for (const device of devices) {
            for (const sensor of device.sensors) {
                const latestResponse = await fetch(`/api/sensors/${sensor.sensor_id}/latest`);
                if (latestResponse.ok) {
                    const reading = await latestResponse.json();
                    const element = document.getElementById(`sensor-${sensor.sensor_id}`);
                    if (element && reading && reading.value !== undefined) {
                        element.textContent = reading.value;
                        element.className = 'sensor-value ' + getStatusClass(reading.value, sensor.type);
                    }
                }
            }
        }
    } catch (error) {
        console.error('Error updating sensor values:', error);
    }
}
function getStatusClass(value, type) {
    if (type === 'temperature') {
        if (value > 30) return 'text-danger';
        if (value > 25) return 'text-warning';
        return 'text-success';
    } else if (type === 'humidity') {
        if (value > 80 || value < 30) return 'text-danger';
        if (value > 70 || value < 40) return 'text-warning';
        return 'text-success';
    } else if (type === 'co2') {
        if (value > 1000) return 'text-danger';
        if (value > 800) return 'text-warning';
        return 'text-success';
    }
    return '';
}
async function updateChartSelectFromDevices() {
    const devicesResponse = await fetch('/api/devices');
    const devices = await devicesResponse.json();
    const select = document.getElementById('chartSensorSelect');
    let html = '<option value="">Pilih sensor untuk grafik</option>';
    let foundSensor = false;
    devices.forEach(device => {
        device.sensors.forEach(sensor => {
            html += `<option value="${sensor.sensor_id}">${device.device_name} - ${sensor.description}</option>`;
            foundSensor = true;
        });
    });
    select.innerHTML = html;
    if (!foundSensor) {
        select.disabled = true;
    } else {
        select.disabled = false;
    }
    select.addEventListener('change', function() {
        if (this.value && typeof loadSensorChart === 'function') {
            loadSensorChart(this.value);
        }
    });
}
window.displayDevices = displayDevices;
window.updateSensorValues = updateSensorValues;
window.getStatusClass = getStatusClass;
window.updateChartSelectFromDevices = updateChartSelectFromDevices; 