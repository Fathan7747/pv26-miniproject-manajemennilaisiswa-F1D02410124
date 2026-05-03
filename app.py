"""
Main Application Window - UI Utama
Menampilkan semua data dan interface utama
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QTabWidget, QMessageBox, QLabel, QStatusBar
)
from PySide6.QtCore import Qt, Slot
from database import DatabaseManager
from controllers import StudentController, GradeController
from dialogs import StudentDialog, GradeDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📊 Manajemen Nilai Siswa")
        self.setGeometry(100, 100, 1400, 700)
        
        # Initialize database and controllers
        self.db = DatabaseManager()
        self.student_controller = StudentController(self.db)
        self.grade_controller = GradeController(self.db)
        
        # Setup UI
        self.setup_ui()
        
        # Create menu bar
        self.create_menu_bar()
        
        # Load stylesheet
        self.load_stylesheet()
        
        # Load initial data
        self.refresh_student_table()
        self.refresh_grade_table()
        
        print("✅ Aplikasi siap digunakan!")
    
    def load_stylesheet(self):
        """Load QSS stylesheet dari file eksternal"""
        try:
            with open("style.qss", "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("⚠️ File style.qss tidak ditemukan. Menggunakan styling default.")
    
    def setup_ui(self):
        """Setup tampilan utama dengan layout manager"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # ===== HEADER dengan info mahasiswa (tidak bisa diedit) =====
        header_layout = QHBoxLayout()
        header_label = QLabel("👤 Nama: Muhammad Fathan Abdullah| NIM: F1D02410124")
        header_label.setObjectName("header_label")
        header_layout.addWidget(header_label)
        header_layout.addStretch()
        main_layout.addLayout(header_layout)
        
        # ===== TAB WIDGET =====
        tabs = QTabWidget()
        
        # ===== TAB 1: STUDENTS =====
        student_tab = QWidget()
        student_layout = QVBoxLayout(student_tab)
        
        # Table untuk menampilkan students
        self.student_table = QTableWidget()
        self.student_table.setColumnCount(6)
        self.student_table.setHorizontalHeaderLabels(["ID", "NIM", "Nama", "Email", "Phone", "Alamat"])
        self.student_table.setColumnHidden(0, True)  # Hide ID column
        self.student_table.setAlternatingRowColors(True)
        student_layout.addWidget(self.student_table)
        
        # Buttons layout untuk Student
        button_layout = QHBoxLayout()
        btn_add_student = QPushButton("➕ Tambah Siswa")
        btn_edit_student = QPushButton("✏️ Edit Siswa")
        btn_delete_student = QPushButton("🗑️ Hapus Siswa")
        btn_refresh = QPushButton("🔄 Refresh")
        
        btn_add_student.clicked.connect(self.add_student_dialog)
        btn_edit_student.clicked.connect(self.edit_student_dialog)
        btn_delete_student.clicked.connect(self.delete_student)
        btn_refresh.clicked.connect(self.refresh_student_table)
        
        button_layout.addWidget(btn_add_student)
        button_layout.addWidget(btn_edit_student)
        button_layout.addWidget(btn_delete_student)
        button_layout.addWidget(btn_refresh)
        button_layout.addStretch()
        student_layout.addLayout(button_layout)
        
        tabs.addTab(student_tab, "📚 Data Siswa")
        
        # ===== TAB 2: GRADES =====
        grade_tab = QWidget()
        grade_layout = QVBoxLayout(grade_tab)
        
        # Table untuk menampilkan grades
        self.grade_table = QTableWidget()
        self.grade_table.setColumnCount(9)
        self.grade_table.setHorizontalHeaderLabels([
            "ID", "Nama Siswa", "NIM", "Mata Pelajaran", 
            "UTS", "UAS", "Tugas", "Total", "Grade"
        ])
        self.grade_table.setColumnHidden(0, True)  # Hide ID column
        self.grade_table.setAlternatingRowColors(True)
        grade_layout.addWidget(self.grade_table)
        
        # Buttons layout untuk Grade
        grade_button_layout = QHBoxLayout()
        btn_add_grade = QPushButton("➕ Tambah Nilai")
        btn_edit_grade = QPushButton("✏️ Edit Nilai")
        btn_delete_grade = QPushButton("🗑️ Hapus Nilai")
        btn_refresh_grade = QPushButton("🔄 Refresh")
        
        btn_add_grade.clicked.connect(self.add_grade_dialog)
        btn_edit_grade.clicked.connect(self.edit_grade_dialog)
        btn_delete_grade.clicked.connect(self.delete_grade)
        btn_refresh_grade.clicked.connect(self.refresh_grade_table)
        
        grade_button_layout.addWidget(btn_add_grade)
        grade_button_layout.addWidget(btn_edit_grade)
        grade_button_layout.addWidget(btn_delete_grade)
        grade_button_layout.addWidget(btn_refresh_grade)
        grade_button_layout.addStretch()
        grade_layout.addLayout(grade_button_layout)
        
        tabs.addTab(grade_tab, "📈 Data Nilai")
        
        main_layout.addWidget(tabs)
        
        # Status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Siap digunakan...")
    
    def create_menu_bar(self):
        """Create menu bar dengan Tentang Aplikasi"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("📁 File")
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)
        
        # Help menu
        help_menu = menubar.addMenu("❓ Help")
        about_action = help_menu.addAction("Tentang Aplikasi")
        about_action.triggered.connect(self.show_about)
    
    def show_about(self):
        """Show about dialog - REQUIREMENT: Menu Tentang Aplikasi"""
        QMessageBox.information(
            self,
            "📊 Tentang Aplikasi",
            "APLIKASI: Manajemen Nilai Siswa\n\n"
            "DESKRIPSI:\n"
            "Aplikasi desktop untuk mengelola data siswa dan nilai mereka.\n"
            "Fitur: CRUD, perhitungan nilai otomatis, penyimpanan database.\n\n"
            "MAHASISWA: Muhammad Fathan Abdullah\n"
            "NIM: F1D02410124\n"
            "KELAS: Pemrograman Visual (PV26)\n\n"
            "TEKNOLOGI:\n"
            "• PySide6 - GUI Framework\n"
            "• SQLite - Database\n"
            "• QSS - Styling\n"
            "• Python 3.8+\n\n"
            "TAHUN: 2026"
        )
    
    # ===== STUDENT OPERATIONS =====
    
    @Slot()
    def add_student_dialog(self):
        """Slot untuk tambah siswa - menggunakan signals/slots"""
        dialog = StudentDialog(self, self.student_controller)
        if dialog.exec():
            self.refresh_student_table()
            self.statusBar.showMessage("✅ Siswa berhasil ditambahkan!", 3000)
    
    @Slot()
    def edit_student_dialog(self):
        """Slot untuk edit siswa - menggunakan signals/slots"""
        current_row = self.student_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "⚠️ Peringatan", "Pilih siswa terlebih dahulu!")
            return
        
        student_id = int(self.student_table.item(current_row, 0).text())
        dialog = StudentDialog(self, self.student_controller, student_id)
        if dialog.exec():
            self.refresh_student_table()
            self.statusBar.showMessage("✅ Siswa berhasil diupdate!", 3000)
    
    @Slot()
    def delete_student(self):
        """Slot untuk hapus siswa dengan konfirmasi QMessageBox"""
        current_row = self.student_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "⚠️ Peringatan", "Pilih siswa terlebih dahulu!")
            return
        
        student_id = int(self.student_table.item(current_row, 0).text())
        student_name = self.student_table.item(current_row, 2).text()
        
        # Konfirmasi dengan QMessageBox
        reply = QMessageBox.question(
            self, "🗑️ Konfirmasi Hapus",
            f"Apakah Anda yakin ingin menghapus siswa '{student_name}'?\n"
            "Data nilai akan ikut terhapus.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.student_controller.delete_student(student_id):
                self.refresh_student_table()
                self.refresh_grade_table()
                self.statusBar.showMessage("✅ Siswa berhasil dihapus!", 3000)
            else:
                QMessageBox.critical(self, "❌ Error", "Gagal menghapus siswa!")
    
    def refresh_student_table(self):
        """Refresh student table - menampilkan data dari database"""
        students = self.student_controller.get_all_students()
        self.student_table.setRowCount(len(students))
        
        for row, student in enumerate(students):
            self.student_table.setItem(row, 0, QTableWidgetItem(str(student["id"])))
            self.student_table.setItem(row, 1, QTableWidgetItem(student["nim"]))
            self.student_table.setItem(row, 2, QTableWidgetItem(student["name"]))
            self.student_table.setItem(row, 3, QTableWidgetItem(student["email"]))
            self.student_table.setItem(row, 4, QTableWidgetItem(student["phone"]))
            self.student_table.setItem(row, 5, QTableWidgetItem(student["address"]))
        
        self.student_table.resizeColumnsToContents()
    
    # ===== GRADE OPERATIONS =====
    
    @Slot()
    def add_grade_dialog(self):
        """Slot untuk tambah nilai - menggunakan signals/slots"""
        students = self.student_controller.get_all_students()
        if not students:
            QMessageBox.warning(self, "⚠️ Peringatan", "Tambahkan siswa terlebih dahulu!")
            return
        
        dialog = GradeDialog(self, self.grade_controller, students)
        if dialog.exec():
            self.refresh_grade_table()
            self.statusBar.showMessage("✅ Nilai berhasil ditambahkan!", 3000)
    
    @Slot()
    def edit_grade_dialog(self):
        """Slot untuk edit nilai - menggunakan signals/slots"""
        current_row = self.grade_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "⚠️ Peringatan", "Pilih nilai terlebih dahulu!")
            return
        
        grade_id = int(self.grade_table.item(current_row, 0).text())
        students = self.student_controller.get_all_students()
        dialog = GradeDialog(self, self.grade_controller, students, grade_id)
        if dialog.exec():
            self.refresh_grade_table()
            self.statusBar.showMessage("✅ Nilai berhasil diupdate!", 3000)
    
    @Slot()
    def delete_grade(self):
        """Slot untuk hapus nilai dengan konfirmasi QMessageBox"""
        current_row = self.grade_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "⚠️ Peringatan", "Pilih nilai terlebih dahulu!")
            return
        
        grade_id = int(self.grade_table.item(current_row, 0).text())
        subject = self.grade_table.item(current_row, 3).text()
        
        # Konfirmasi dengan QMessageBox
        reply = QMessageBox.question(
            self, "🗑️ Konfirmasi Hapus",
            f"Apakah Anda yakin ingin menghapus nilai untuk '{subject}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.grade_controller.delete_grade(grade_id):
                self.refresh_grade_table()
                self.statusBar.showMessage("✅ Nilai berhasil dihapus!", 3000)
            else:
                QMessageBox.critical(self, "❌ Error", "Gagal menghapus nilai!")
    
    def refresh_grade_table(self):
        """Refresh grade table - menampilkan data dari database"""
        grades = self.grade_controller.get_all_grades()
        self.grade_table.setRowCount(len(grades))
        
        for row, grade in enumerate(grades):
            self.grade_table.setItem(row, 0, QTableWidgetItem(str(grade["id"])))
            self.grade_table.setItem(row, 1, QTableWidgetItem(grade["name"]))
            self.grade_table.setItem(row, 2, QTableWidgetItem(grade["nim"]))
            self.grade_table.setItem(row, 3, QTableWidgetItem(grade["subject"]))
            self.grade_table.setItem(row, 4, QTableWidgetItem(f"{grade['midterm']:.1f}"))
            self.grade_table.setItem(row, 5, QTableWidgetItem(f"{grade['final']:.1f}"))
            self.grade_table.setItem(row, 6, QTableWidgetItem(f"{grade['assignment']:.1f}"))
            self.grade_table.setItem(row, 7, QTableWidgetItem(f"{grade['total']:.2f}"))
            self.grade_table.setItem(row, 8, QTableWidgetItem(grade["grade_letter"]))
        
        self.grade_table.resizeColumnsToContents()
