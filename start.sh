#!/bin/bash

echo "========================================"
echo "SISTEM PEMANTAUAN LINGKUNGAN IoT"
echo "========================================"
echo

echo "[1/4] Memeriksa dependensi..."
python3 -c "import flask, pymongo, requests, pandas, numpy, matplotlib" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
else
    echo "Dependencies OK"
fi

echo
echo "[2/4] Memeriksa MongoDB..."
python3 -c "from pymongo import MongoClient; client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=3000); client.server_info(); print('MongoDB OK')" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "WARNING: MongoDB tidak terhubung"
    echo "Pastikan MongoDB berjalan di localhost:27017"
    echo
fi

echo
echo "[3/4] Menjalankan sistem..."
echo
python3 run_system.py

echo
echo "[4/4] Sistem selesai" 