function getStatusText(value, type) {
    if (type === 'temperature') {
        if (value > 30) return 'Panas';
        if (value > 25) return 'Hangat';
        return 'Normal';
    } else if (type === 'humidity') {
        if (value > 80 || value < 30) return 'Ekstrem';
        if (value > 70 || value < 40) return 'Tinggi/Rendah';
        return 'Normal';
    } else if (type === 'co2') {
        if (value > 1000) return 'Berbahaya';
        if (value > 800) return 'Tinggi';
        return 'Normal';
    }
    return 'Normal';
}
function displayReadingsTable(readings) {
    const tbody = document.getElementById('readingsTable');
    let html = '';
    readings.forEach(reading => {
        const timestamp = new Date(reading.timestamp).toLocaleString('id-ID');
        const statusText = getStatusText(reading.value, reading.sensor_type);
        let badgeClass = 'badge-secondary';
        if (statusText === 'Normal') badgeClass = 'badge-normal';
        else if (statusText === 'Hangat' || statusText === 'Tinggi/Rendah') badgeClass = 'badge-warning';
        else if (statusText === 'Panas' || statusText === 'Tinggi' || statusText === 'Berbahaya' || statusText === 'Ekstrem') badgeClass = 'badge-danger';
        html += `
            <tr>
                <td>${reading.device_id}</td>
                <td>${reading.sensor_id}</td>
                <td>${reading.sensor_type}</td>
                <td><strong>${reading.value} ${reading.unit}</strong></td>
                <td>${timestamp}</td>
                <td><span class="badge badge-status ${badgeClass}">${statusText}</span></td>
            </tr>
        `;
    });
    tbody.innerHTML = html;
}
function updatePaginationInfo(page, totalPages, total) {
    document.getElementById('paginationInfo').textContent = `Halaman ${page} dari ${totalPages} | Total: ${total}`;
    document.getElementById('prevPageBtn').disabled = page <= 1;
    document.getElementById('nextPageBtn').disabled = page >= totalPages;
}
async function loadLatestReadings(page = 1) {
    const devicesResponse = await fetch('/api/devices');
    const devices = await devicesResponse.json();
    let device_id = devices.length > 0 ? devices[0].device_id : null;
    if (!device_id) {
        displayReadingsTable([]);
        updatePaginationInfo(1, 1, 0);
        return;
    }
    let url = `/api/devices/${device_id}/readings?page=${page}&per_page=10`;
    const readingsResponse = await fetch(url);
    let allReadings = [];
    let total = 0;
    if (readingsResponse.ok) {
        const result = await readingsResponse.json();
        allReadings = result.data;
        currentPage = result.page;
        totalPages = result.total_pages;
        total = result.total;
    }
    displayReadingsTable(allReadings);
    updatePaginationInfo(currentPage, totalPages, total);
}
function addSortToTable() {
    document.querySelectorAll('th.sortable').forEach(th => {
        th.style.cursor = 'pointer';
        th.addEventListener('click', function() {
            const field = th.getAttribute('data-field');
            // Sorting logic bisa ditambahkan di sini jika diinginkan
        });
    });
}
async function applyAdvancedFilter() {
    const start = document.getElementById('filterStart').value;
    const end = document.getElementById('filterEnd').value;
    const threshold = document.getElementById('filterThreshold').value;
    const status = document.getElementById('filterStatus').value;
    const alertBox = document.getElementById('filterAlertBox');
    alertBox.innerHTML = "";
    const devicesResponse = await fetch('/api/devices');
    const devices = await devicesResponse.json();
    if (devices.length === 0) {
        alertBox.innerHTML = `<div class="alert alert-danger">Tidak ada perangkat.</div>`;
        return;
    }
    const device_id = devices[0].device_id;
    const sensor_id = devices[0].sensors[0].sensor_id;
    let url = `/api/devices/${device_id}/readings/range?start=${start}&end=${end}`;
    const readings = await (await fetch(url)).json();
    let filteredReadings = readings;
    if (status) {
        filteredReadings = readings.filter(r => getStatusText(r.value, r.sensor_type) === status);
    }
    displayReadingsTable(filteredReadings);
    let statsUrl = `/api/devices/${device_id}/sensors/${sensor_id}/stats?start=${start}&end=${end}`;
    const stats = await (await fetch(statsUrl)).json();
    alertBox.innerHTML += stats && stats.count > 0 ?
        `<div class="alert alert-info mb-2">
            <strong>Statistik Sensor:</strong><br>
            Rata-rata: <b>${stats.avg?.toFixed(2) ?? '-'}</b>,
            Min: <b>${stats.min ?? '-'}</b>,
            Max: <b>${stats.max ?? '-'}</b>,
            Stddev: <b>${stats.stddev?.toFixed(2) ?? '-'}</b>
        </div>` :
        `<div class="alert alert-warning mb-2">Tidak ada data statistik pada periode ini.</div>`;
    if (threshold && filteredReadings.length > 0) {
        let alertUrl = `/api/alerts/threshold?type=${filteredReadings[0].sensor_type}&threshold=${threshold}&start=${start}&end=${end}`;
        const alerts = await (await fetch(alertUrl)).json();
        if (alerts.length > 0) {
            alertBox.innerHTML += `
                <div class="alert alert-danger">
                    <strong>Perangkat melebihi ambang batas:</strong>
                    <ul>
                        ${alerts.map(a => `<li>${a._id} (Nilai Maks: ${a.max_value})</li>`).join('')}
                    </ul>
                </div>
            `;
        } else {
            alertBox.innerHTML += `<div class="alert alert-success">Tidak ada perangkat yang melebihi ambang batas.</div>`;
        }
    }
}
window.getStatusText = getStatusText;
window.displayReadingsTable = displayReadingsTable;
window.updatePaginationInfo = updatePaginationInfo;
window.loadLatestReadings = loadLatestReadings;
window.addSortToTable = addSortToTable;
window.applyAdvancedFilter = applyAdvancedFilter; 