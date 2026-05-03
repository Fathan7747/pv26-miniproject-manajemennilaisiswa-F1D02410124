# miniproject_PV26_F1D02410124_MuhammadFathanAbdullah


# 📊 Manajemen Nilai Siswa

Aplikasi desktop untuk mengelola data siswa dan nilai mereka menggunakan **PySide6** dan **SQLite**.

## 📋 Deskripsi

Aplikasi ini menyediakan fitur lengkap untuk:
- ✅ Menambah, mengubah, menghapus data siswa (5 field: NIM, Nama, Email, Phone, Alamat)
- ✅ Mengelola nilai siswa untuk berbagai mata pelajaran
- ✅ Menampilkan perhitungan nilai otomatis (UTS 30%, UAS 50%, Tugas 20%)
- ✅ Penyimpanan data permanen dengan SQLite
- ✅ Antarmuka yang intuitif dan responsif dengan tema modern
- ✅ Signals/Slots untuk interaksi komponen
- ✅ Styling dengan QSS eksternal
- ✅ Separation of Concerns (SoC) - kode terstruktur dengan baik

**Database dibuat otomatis** saat aplikasi dijalankan pertama kali. Semua data akan tersimpan permanen dan tidak akan hilang setelah aplikasi ditutup.

## 🛠️ Teknologi yang Digunakan

| Teknologi | Versi | Keterangan |
|-----------|-------|-----------|
| Python | 3.8+ | Programming Language |
| PySide6 | Latest | Qt Framework untuk GUI |
| SQLite | 3 | Database |
| QSS | N/A | Styling untuk Qt |

## 📁 Struktur Project

```
miniproject/
├── main.py              # Entry point aplikasi
├── app.py              # Main window UI
├── dialogs.py          # Form dialogs (StudentDialog, GradeDialog)
├── database.py         # Database operations (SQLite)
├── controllers.py      # Business logic (StudentController, GradeController)
├── style.qss           # Styling eksternal
├── README.md           # Dokumentasi ini
├── .gitignore          # Git configuration
└── students_grades.db  # Database (auto-dibuat saat run pertama)
```

## 🚀 Cara Menjalankan

### Persyaratan
- Python 3.8 atau lebih tinggi
- pip (Python package manager)

### Step 1: Install Python
Pastikan Python sudah terinstall. Cek dengan:
```bash
python --version
```

### Step 2: Install PySide6
Buka Command Prompt/Terminal dan jalankan:
```bash
pip install PySide6
```

### Step 3: Clone atau Download Project
Download project ini dan ekstrak ke folder yang diinginkan.

### Step 4: Jalankan Aplikasi
Buka Command Prompt/Terminal, masuk ke folder project:
```bash
cd path/to/miniproject
```

Kemudian jalankan:
```bash
python main.py
```

**PENTING:** Pastikan Command Prompt/Terminal di-buka dari folder yang sama dengan `main.py`.

### Output Saat Aplikasi Pertama Kali Dijalankan
```
============================================================
🚀 Starting Manajemen Nilai Siswa Application
============================================================
📁 Current directory: D:\...\miniproject
📂 Project files location: D:\...\miniproject
============================================================
📂 Database path: D:\...\miniproject\students_grades.db
📝 Creating students table...
✅ Students table created!
📝 Creating grades table...
✅ Grades table created!
✅ Database initialized successfully!
============================================================
✅ Application loaded successfully!
============================================================
```

**File `students_grades.db` akan otomatis dibuat** di folder yang sama dengan `main.py`.

## ✨ Fitur Utama

### 1. 📚 Manajemen Siswa
- **Tambah Siswa**: Form dengan 5 input fields (NIM, Nama, Email, Phone, Alamat)
- **Edit Siswa**: Ubah data siswa yang sudah ada
- **Hapus Siswa**: Hapus siswa dengan konfirmasi QMessageBox
- **Validasi**: Email harus valid, semua field harus diisi
- **Display**: Tabel QTableWidget menampilkan semua siswa

### 2. 📈 Manajemen Nilai
- **Tambah Nilai**: Form dengan 5 input fields (Siswa, Mata Pelajaran, UTS, UAS, Tugas)
- **Edit Nilai**: Ubah nilai yang sudah ada
- **Hapus Nilai**: Hapus nilai dengan konfirmasi
- **Perhitungan Otomatis**: Total = (UTS × 30%) + (UAS × 50%) + (Tugas × 20%)
- **Grade Otomatis**:
  - A: ≥ 85
  - B: 75-84
  - C: 65-74
  - D: 55-64
  - E: < 55

### 3. 🗄️ Database SQLite
- **Tabel Students**: 7 kolom (id, nim, name, email, phone, address, created_at)
- **Tabel Grades**: 9 kolom (id, student_id, subject, midterm, final, assignment, total, grade_letter, created_at)
- **Auto Create**: Database dan tabel dibuat otomatis saat run pertama
- **Data Persistence**: Data tetap tersimpan bahkan setelah aplikasi ditutup

### 4. 🎨 UI/UX
- **Tab Widget**: Navigasi antara Siswa dan Nilai
- **QTableWidget**: Display data dalam format tabel
- **Menu Bar**: File menu (Exit) dan Help menu (About)
- **Status Bar**: Feedback status operasi
- **QMessageBox**: Dialog untuk konfirmasi dan validasi
- **Responsive Layout**: QVBoxLayout, QHBoxLayout, QFormLayout
- **Modern Styling**: QSS eksternal dengan warna profesional

### 5. 🔌 Signals & Slots
- Button clicks terhubung ke methods
- Value changed untuk perhitungan real-time
- Dialog exec untuk form modal

## 📊 Database Schema

### Tabel `students`
Menyimpan data siswa dengan 7 kolom:

| Kolom | Tipe | Keterangan |
|-------|------|-----------|
| id | INTEGER | Primary key, auto-increment |
| nim | TEXT | Nomor induk siswa (UNIQUE) |
| name | TEXT | Nama lengkap siswa |
| email | TEXT | Email siswa |
| phone | TEXT | Nomor telepon siswa |
| address | TEXT | Alamat tinggal siswa |
| created_at | TIMESTAMP | Waktu data dibuat |

**Contoh Data:**
```
id | nim | name        | email              | phone        | address
1  | 001 | Ahmad Aji   | ahmad@gmail.com    | 08123456789  | Jl. Merdeka 123
2  | 002 | Budi Santoso| budi@gmail.com     | 08234567890  | Jl. Sudirman 456
```

### Tabel `grades`
Menyimpan data nilai siswa dengan 9 kolom:

| Kolom | Tipe | Keterangan |
|-------|------|-----------|
| id | INTEGER | Primary key, auto-increment |
| student_id | INTEGER | Foreign key ke tabel students |
| subject | TEXT | Nama mata pelajaran |
| midterm | REAL | Nilai UTS (0-100) |
| final | REAL | Nilai UAS (0-100) |
| assignment | REAL | Nilai tugas (0-100) |
| total | REAL | Total nilai (perhitungan otomatis) |
| grade_letter | TEXT | Grade huruf (A/B/C/D/E) |
| created_at | TIMESTAMP | Waktu data dibuat |

**Contoh Data:**
```
id | student_id | subject | midterm | final | assignment | total | grade_letter
1  | 1          | Matkul1 | 80      | 85    | 75         | 81.5  | B
2  | 1          | Matkul2 | 90      | 88    | 92         | 89.4  | A
```

## 🏗️ Penerapan Separation of Concerns (SoC)

Kode diorganisir ke dalam 6 layer yang terpisah:

### 1. **main.py** - Entry Point
File yang dijalankan pertama kali. Membuat QApplication dan MainWindow.

### 2. **app.py** - Presentation Layer
UI utama aplikasi (MainWindow). Setup layout, tab, table, buttons, menu bar. Tidak mengandung business logic database.

### 3. **dialogs.py** - Dialog Components
StudentDialog dan GradeDialog untuk form input. Terpisah dari main window.

### 4. **controllers.py** - Business Logic Layer
StudentController dan GradeController. Handle validasi dan logic sebelum ke database.

### 5. **database.py** - Data Access Layer
DatabaseManager. Langsung berinteraksi dengan SQLite. CRUD operations.

### 6. **style.qss** - Styling Layer
Styling eksternal. Pisah dari code Python, mudah di-customize.

**Alur Aliran Data:**
```
User Action (View) 
    ↓
Button Click Signal (app.py)
    ↓
Dialog Form (dialogs.py)
    ↓
User Input Validation (dialogs.py)
    ↓
Call Controller (controllers.py)
    ↓
Business Logic & Validation (controllers.py)
    ↓
Call Database (database.py)
    ↓
Execute SQL Query (database.py)
    ↓
SQLite Database (students_grades.db)
    ↓
Return Result
    ↓
Update UI (app.py)
    ↓
Refresh Table (app.py)
```

## 📋 Checklist Fitur Wajib

✅ **Form input minimal 5 field**
   - StudentDialog: NIM, Nama, Email, Phone, Alamat
   - GradeDialog: Siswa, Mata Pelajaran, UTS, UAS, Tugas

✅ **Interaksi komponen menggunakan signals dan slots**
   - Button clicked signals
   - Value changed signals
   - Dialog exec signals

✅ **Layout rapi dan terstruktur**
   - QVBoxLayout, QHBoxLayout, QFormLayout
   - Tab Widget untuk navigasi
   - Menu bar dan status bar

✅ **Tampilan data menggunakan QTableWidget**
   - Tabel Siswa (6 kolom)
   - Tabel Nilai (9 kolom)
   - Sorting dan resizing otomatis

✅ **Integrasi SQLite dengan CRUD**
   - Create: add_student(), add_grade()
   - Read: get_all_students(), get_all_grades()
   - Update: update_student(), update_grade()
   - Delete: delete_student(), delete_grade()
   - Data tetap tersimpan

✅ **Menu bar dengan Tentang Aplikasi**
   - File menu (Exit)
   - Help menu (About)
   - Info: Nama App, Deskripsi, Nama Mahasiswa, NIM

✅ **Form tambah/edit di dialog terpisah**
   - StudentDialog untuk form siswa
   - GradeDialog untuk form nilai
   - Main window hanya display data

✅ **Minimal satu dialog konfirmasi**
   - QMessageBox warning saat ada error
   - QMessageBox info saat sukses
   - QMessageBox question saat hapus (Yes/No)

✅ **Nama dan NIM tampil non-editable**
   - Header: "👤 Nama: Fathan7747 | NIM: F1D123456"
   - Tidak bisa diedit user

✅ **Styling QSS eksternal**
   - File style.qss terpisah
   - Button styling, table styling, input styling
   - Hover effects dan active states

✅ **Struktur project SoC**
   - 6 file terpisah dengan tanggung jawab spesifik
   - UI, Logic, Database, Styling layer terpisah
   - Code modular dan mudah di-extend

## 🎓 Informasi Pengembang

| Item | Detail |
|------|--------|
| **Nama** | Fathan7747 |
| **NIM** | F1D123456 |
| **Kelas** | PV26 |
| **Tugas** | Mini Project - Manajemen Nilai Siswa |
| **Universitas** | Teknik Informatika S1 |

## 🐛 Troubleshooting

### Error: `ModuleNotFoundError: No module named 'PySide6'`
**Solusi:** Install PySide6 dengan:
```bash
pip install PySide6
```

### Error: `FileNotFoundError: style.qss`
**Solusi:** Pastikan file `style.qss` ada di folder yang sama dengan `main.py`.

### Database tidak muncul
**Solusi:** File `students_grades.db` akan otomatis dibuat di folder project saat aplikasi dijalankan. Pastikan folder writable.

### Data tidak tersimpan setelah close aplikasi
**Solusi:** Data disimpan di SQLite, tidak perlu manual save. Cek file `students_grades.db` ada di folder.

## 📚 Referensi

- [PySide6 Documentation](https://doc.qt.io/qtforpython/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Qt Documentation](https://doc.qt.io/)

## 📄 Lisensi

MIT License - 2026

---

**Terima kasih telah menggunakan aplikasi ini!** 🎉
