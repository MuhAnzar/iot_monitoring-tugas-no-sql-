#!/usr/bin/env python3
"""
Analisis Data Sensor IoT - Sistem Pemantauan Lingkungan
Menganalisis data sensor dan generate laporan statistik
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple
import json

class SensorDataAnalyzer:
    def __init__(self, api_base_url: str = "http://localhost:5000/api"):
        self.api_base_url = api_base_url
        
    def get_sensor_data(self, sensor_id: str, hours: int = 24) -> pd.DataFrame:
        """Mengambil data sensor dari API dan convert ke DataFrame"""
        try:
            # Hitung waktu mulai dan selesai
            end_time = datetime.now()
            start_time = end_time - timedelta(hours=hours)
            
            # Ambil data dari API
            params = {
                'start_time': start_time.isoformat(),
                'end_time': end_time.isoformat(),
                'limit': 1000
            }
            
            response = requests.get(f"{self.api_base_url}/sensors/{sensor_id}/readings", params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                # Convert ke DataFrame
                df = pd.DataFrame(data)
                if not df.empty:
                    df['timestamp'] = pd.to_datetime(df['timestamp'])
                    df['value'] = pd.to_numeric(df['value'])
                    df = df.sort_values('timestamp')
                
                return df
            else:
                print(f"❌ Error mengambil data sensor {sensor_id}: {response.status_code}")
                return pd.DataFrame()
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return pd.DataFrame()
    
    def get_all_devices_data(self, hours: int = 24) -> Dict[str, pd.DataFrame]:
        """Mengambil data dari semua perangkat"""
        try:
            # Ambil daftar perangkat
            response = requests.get(f"{self.api_base_url}/devices")
            if response.status_code != 200:
                print("❌ Error mengambil daftar perangkat")
                return {}
            
            devices = response.json()
            all_data = {}
            
            for device in devices:
                device_id = device['device_id']
                print(f"📊 Mengambil data untuk perangkat: {device['device_name']}")
                
                for sensor in device['sensors']:
                    sensor_id = sensor['sensor_id']
                    df = self.get_sensor_data(sensor_id, hours)
                    if not df.empty:
                        all_data[sensor_id] = df
            
            return all_data
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return {}
    
    def calculate_statistics(self, df: pd.DataFrame) -> Dict:
        """Menghitung statistik dasar dari data sensor"""
        if df.empty:
            return {}
        
        stats = {
            'count': len(df),
            'mean': df['value'].mean(),
            'median': df['value'].median(),
            'std': df['value'].std(),
            'min': df['value'].min(),
            'max': df['value'].max(),
            'range': df['value'].max() - df['value'].min(),
            'first_reading': df['timestamp'].min(),
            'last_reading': df['timestamp'].max(),
            'time_span_hours': (df['timestamp'].max() - df['timestamp'].min()).total_seconds() / 3600
        }
        
        return stats
    
    def detect_anomalies(self, df: pd.DataFrame, threshold_std: float = 2.0) -> pd.DataFrame:
        """Deteksi anomali menggunakan metode statistical outlier"""
        if df.empty:
            return pd.DataFrame()
        
        # Hitung z-score
        mean = df['value'].mean()
        std = df['value'].std()
        df['z_score'] = (df['value'] - mean) / std
        
        # Deteksi outlier
        anomalies = df[abs(df['z_score']) > threshold_std].copy()
        anomalies['anomaly_type'] = 'outlier'
        
        return anomalies
    
    def analyze_trends(self, df: pd.DataFrame) -> Dict:
        """Analisis tren data sensor"""
        if df.empty or len(df) < 2:
            return {}
        
        # Linear regression untuk trend
        x = np.arange(len(df))
        y = df['value'].values
        
        # Hitung slope (trend)
        slope = np.polyfit(x, y, 1)[0]
        
        # Hitung perubahan total
        total_change = df['value'].iloc[-1] - df['value'].iloc[0]
        
        # Hitung rata-rata perubahan per jam
        time_diff_hours = (df['timestamp'].max() - df['timestamp'].min()).total_seconds() / 3600
        change_per_hour = total_change / time_diff_hours if time_diff_hours > 0 else 0
        
        trends = {
            'slope': slope,
            'total_change': total_change,
            'change_per_hour': change_per_hour,
            'trend_direction': 'increasing' if slope > 0 else 'decreasing' if slope < 0 else 'stable',
            'trend_strength': abs(slope)
        }
        
        return trends
    
    def generate_report(self, hours: int = 24) -> Dict:
        """Generate laporan lengkap analisis data"""
        print("📊 Memulai analisis data sensor...")
        
        # Ambil semua data
        all_data = self.get_all_devices_data(hours)
        
        if not all_data:
            print("❌ Tidak ada data yang dapat dianalisis")
            return {}
        
        report = {
            'analysis_timestamp': datetime.now().isoformat(),
            'analysis_period_hours': hours,
            'total_sensors': len(all_data),
            'sensors': {}
        }
        
        total_readings = 0
        total_anomalies = 0
        
        for sensor_id, df in all_data.items():
            print(f"🔍 Menganalisis sensor: {sensor_id}")
            
            # Hitung statistik
            stats = self.calculate_statistics(df)
            
            # Deteksi anomali
            anomalies = self.detect_anomalies(df)
            
            # Analisis tren
            trends = self.analyze_trends(df)
            
            # Simpan hasil analisis
            sensor_analysis = {
                'statistics': stats,
                'trends': trends,
                'anomalies_count': len(anomalies),
                'anomalies': anomalies.to_dict('records') if not anomalies.empty else []
            }
            
            report['sensors'][sensor_id] = sensor_analysis
            total_readings += stats.get('count', 0)
            total_anomalies += len(anomalies)
        
        # Tambahkan ringkasan
        report['summary'] = {
            'total_readings': total_readings,
            'total_anomalies': total_anomalies,
            'anomaly_rate': (total_anomalies / total_readings * 100) if total_readings > 0 else 0
        }
        
        return report
    
    def plot_sensor_data(self, sensor_id: str, hours: int = 24, save_path: str = None):
        """Plot data sensor dengan matplotlib"""
        df = self.get_sensor_data(sensor_id, hours)
        
        if df.empty:
            print(f"❌ Tidak ada data untuk sensor {sensor_id}")
            return
        
        # Setup plot
        plt.figure(figsize=(12, 8))
        
        # Plot utama
        plt.subplot(2, 1, 1)
        plt.plot(df['timestamp'], df['value'], 'b-', linewidth=2, label='Sensor Reading')
        
        # Deteksi dan plot anomali
        anomalies = self.detect_anomalies(df)
        if not anomalies.empty:
            plt.scatter(anomalies['timestamp'], anomalies['value'], 
                       color='red', s=50, label='Anomalies', zorder=5)
        
        plt.title(f'Sensor Data Analysis: {sensor_id}')
        plt.xlabel('Time')
        plt.ylabel('Value')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Plot histogram
        plt.subplot(2, 1, 2)
        plt.hist(df['value'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
        plt.title('Value Distribution')
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"📊 Plot disimpan ke: {save_path}")
        else:
            plt.show()
        
        plt.close()
    
    def save_report(self, report: Dict, filename: str = None):
        """Simpan laporan ke file JSON"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"sensor_analysis_report_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, default=str)
            print(f"📄 Laporan disimpan ke: {filename}")
        except Exception as e:
            print(f"❌ Error menyimpan laporan: {e}")
    
    def print_summary(self, report: Dict):
        """Print ringkasan laporan"""
        if not report:
            print("❌ Tidak ada laporan untuk ditampilkan")
            return
        
        print("\n" + "="*60)
        print("📊 LAPORAN ANALISIS DATA SENSOR IoT")
        print("="*60)
        
        summary = report.get('summary', {})
        print(f"📈 Total Pembacaan: {summary.get('total_readings', 0):,}")
        print(f"⚠️  Total Anomali: {summary.get('total_anomalies', 0)}")
        print(f"📊 Tingkat Anomali: {summary.get('anomaly_rate', 0):.2f}%")
        print(f"⏰ Periode Analisis: {report.get('analysis_period_hours', 0)} jam")
        print(f"🔍 Jumlah Sensor: {report.get('total_sensors', 0)}")
        
        print("\n📋 DETAIL PER SENSOR:")
        print("-" * 60)
        
        for sensor_id, analysis in report.get('sensors', {}).items():
            stats = analysis.get('statistics', {})
            trends = analysis.get('trends', {})
            
            print(f"\n🔸 Sensor: {sensor_id}")
            print(f"   📊 Rata-rata: {stats.get('mean', 0):.2f}")
            print(f"   📈 Min-Max: {stats.get('min', 0):.2f} - {stats.get('max', 0):.2f}")
            print(f"   📉 Standar Deviasi: {stats.get('std', 0):.2f}")
            print(f"   🔄 Tren: {trends.get('trend_direction', 'unknown')}")
            print(f"   ⚠️  Anomali: {analysis.get('anomalies_count', 0)}")

def main():
    """Main function untuk menjalankan analisis data"""
    print("🔬 Sensor Data Analyzer - Sistem Pemantauan Lingkungan IoT")
    print("=" * 60)
    
    analyzer = SensorDataAnalyzer()
    
    # Generate laporan
    print("📊 Menggenerate laporan analisis data...")
    report = analyzer.generate_report(hours=24)
    
    if report:
        # Print ringkasan
        analyzer.print_summary(report)
        
        # Simpan laporan
        analyzer.save_report(report)
        
        # Plot beberapa sensor sebagai contoh
        print("\n📈 Menggenerate plot untuk beberapa sensor...")
        for sensor_id in list(report.get('sensors', {}).keys())[:3]:  # Plot 3 sensor pertama
            analyzer.plot_sensor_data(sensor_id, hours=24, 
                                   save_path=f"plot_{sensor_id}.png")
        
        print("\n✅ Analisis data selesai!")
    else:
        print("❌ Gagal menggenerate laporan")

if __name__ == "__main__":
    main() 