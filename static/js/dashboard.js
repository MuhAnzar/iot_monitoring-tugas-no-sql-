document.addEventListener('DOMContentLoaded', function() {
    if (typeof loadDashboardData === 'function') {
        loadDashboardData();
        setInterval(loadDashboardData, 30000);
    }
    if (typeof updateSensorValues === 'function') {
        updateSensorValues();
    }
    if (typeof addSortToTable === 'function') {
        addSortToTable();
    }
    if (typeof updateChartSelectFromDevices === 'function') {
        updateChartSelectFromDevices();
    }
}); 