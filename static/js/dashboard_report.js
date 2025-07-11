async function generateReport() {
    const device_id = document.getElementById('reportDevice').value;
    const sensor_id = document.getElementById('reportSensor').value;
    const start = document.getElementById('reportStart').value;
    const end = document.getElementById('reportEnd').value;
    const threshold = document.getElementById('reportThreshold').value;
    // Ambil info perangkat
    const devices = await (await fetch('/api/devices')).json();
    const device = devices.find(d => d.device_id === device_id);
    const sensor = device ? device.sensors.find(s => s.sensor_id === sensor_id) : null;
    // Fetch laporan
    let url = `/api/report?device_id=${device_id}&sensor_id=${sensor_id}&start=${start}&end=${end}&threshold=${threshold}`;
    const report = await (await fetch(url)).json();
    let html = '';
    // Info perangkat & sensor
    let info = '<div class="row mb-3">';
    if (device) {
        info += `<div class="col-md-6"><b>Perangkat:</b> ${device.device_name} <br><b>ID:</b> ${device.device_id}<br><b>Lokasi:</b> ${device.location}</div>`;
    }
    if (sensor) {
        info += `<div class="col-md-6"><b>Sensor:</b> ${sensor.description} <br><b>ID:</b> ${sensor.sensor_id}<br><b>Tipe:</b> ${sensor.type} (${sensor.unit})</div>`;
    }
    info += '</div>';
    document.getElementById('laporanDeviceInfo').innerHTML = info;
    // Statistik (info box grid)
    if (report.stats && report.stats.count > 0) {
        html += `<div class="row text-center mb-3">
            <div class="col-6 col-md-3">
                <div class="info-box avg"><i class="fas fa-chart-line"></i> Rata-rata<br>${report.stats.avg?.toFixed(2) ?? '-'} ${sensor ? sensor.unit : ''}</div>
            </div>
            <div class="col-6 col-md-3">
                <div class="info-box min"><i class="fas fa-arrow-down"></i> Min<br>${report.stats.min ?? '-'} ${sensor ? sensor.unit : ''}</div>
            </div>
            <div class="col-6 col-md-3">
                <div class="info-box max"><i class="fas fa-arrow-up"></i> Max<br>${report.stats.max ?? '-'} ${sensor ? sensor.unit : ''}</div>
            </div>
            <div class="col-6 col-md-3">
                <div class="info-box stddev"><i class="fas fa-wave-square"></i> Stddev<br>${report.stats.stddev?.toFixed(2) ?? '-'} ${sensor ? sensor.unit : ''}</div>
            </div>
        </div>`;
    } else {
        html += `<div class="alert alert-warning mb-2">Tidak ada data statistik pada periode ini.</div>`;
    }
    // Perangkat melebihi ambang batas
    if (report.exceed && report.exceed.length > 0) {
        html += `<div class="alert alert-danger mb-2"><b>Perangkat melebihi ambang batas:</b><ul class='mb-0'>`;
        report.exceed.forEach(e => {
            html += `<li>${e.device_id} (Nilai Maks: ${e.max_value})</li>`;
        });
        html += `</ul></div>`;
    } else if (threshold) {
        html += `<div class="alert alert-success mb-2">Tidak ada perangkat yang melebihi ambang batas.</div>`;
    }
    // Tabel data pembacaan
    if (report.readings && report.readings.length > 0) {
        html += `<div class="table-responsive"><table class="table table-bordered table-sm align-middle">
            <thead class="table-light sticky-top">
                <tr>
                    <th>Perangkat</th>
                    <th>Waktu</th>
                    <th>Status</th>
                    <th>Suhu</th>
                </tr>
            </thead>
            <tbody>`;
        report.readings.forEach(r => {
            let deviceName = device ? device.device_name : (r.device_id || '-');
            let suhu = '';
            if (sensor && sensor.type === 'temperature') {
                suhu = r.value + ' ' + (sensor.unit || '');
            } else if (r.sensor_type === 'temperature') {
                suhu = r.value + ' ' + (r.unit || '');
            }
            let status = window.getStatusText ? getStatusText(r.value, r.sensor_type) : (r.status || '-');
            let badgeClass = 'badge-secondary';
            if (status === 'Normal') badgeClass = 'badge-normal';
            else if (status === 'Hangat' || status === 'Tinggi/Rendah') badgeClass = 'badge-warning text-dark';
            else if (status === 'Panas' || status === 'Tinggi' || status === 'Berbahaya' || status === 'Ekstrem') badgeClass = 'badge-danger';
            html += `<tr>
                <td>${deviceName}</td>
                <td>${new Date(r.timestamp).toLocaleString('id-ID')}</td>
                <td><span class="badge badge-status ${badgeClass}">${status}</span></td>
                <td>${suhu}</td>
            </tr>`;
        });
        html += `</tbody></table></div>`;
    } else {
        html += `<div class="alert alert-info">Tidak ada data pembacaan pada periode ini.</div>`;
    }
    document.getElementById('laporanContent').innerHTML = html;
    document.getElementById('laporanSection').style.display = '';
    document.getElementById('reportResultBox').innerHTML = '';
    var modal = bootstrap.Modal.getInstance(document.getElementById('reportModal'));
    modal.hide();
}
function downloadReportCSV() {
    const device_id = document.getElementById('reportDevice').value;
    const sensor_id = document.getElementById('reportSensor').value;
    const start = document.getElementById('reportStart').value;
    const end = document.getElementById('reportEnd').value;
    const threshold = document.getElementById('reportThreshold').value;
    let url = `/api/report/download?device_id=${device_id}&sensor_id=${sensor_id}&start=${start}&end=${end}&threshold=${threshold}`;
    window.open(url, '_blank');
}
function closeLaporan() {
    document.getElementById('laporanSection').style.display = 'none';
}
window.generateReport = generateReport;
window.downloadReportCSV = downloadReportCSV;
window.closeLaporan = closeLaporan; 