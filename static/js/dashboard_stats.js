function updateStatistics(stats) {
    document.getElementById('totalDevices').textContent = stats.total_devices;
    document.getElementById('totalReadings').textContent = stats.total_readings.toLocaleString();
    document.getElementById('activeSensors').textContent = Object.keys(stats.latest_readings).length;
}
window.updateStatistics = updateStatistics; 