"""
MANAJEMEN NILAI SISWA - PySide6 Application
Topik: Manajemen Nilai Siswa
Mahasiswa: Muhammad Fathan Abdullah | NIM: F1D02410124
"""
import sys
import os
from PySide6.QtWidgets import QApplication
from app import MainWindow

def main():
    print("=" * 60)
    print(" Starting Manajemen Nilai Siswa Application")
    print("=" * 60)
    print(f" Current directory: {os.getcwd()}")
    print(f" Project files location: {os.path.abspath('.')}")
    print("=" * 60)
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    print("=" * 60)
    print("✅ Application loaded successfully!")
    print("=" * 60)
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
