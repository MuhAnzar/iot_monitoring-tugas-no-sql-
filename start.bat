@echo off
echo ========================================
echo SISTEM PEMANTAUAN LINGKUNGAN IoT
echo ========================================
echo.

echo [1/4] Setup otomatis...
python setup.py

echo.
echo [2/4] Jika setup berhasil, sistem akan berjalan
echo Dashboard: http://localhost:5000
echo API: http://localhost:5000/api
echo.

echo [3/4] Untuk menjalankan IoT Simulator terpisah:
echo python run_simulator.py
echo.

echo [4/4] Untuk test API:
echo python test_api.py
echo.

pause 