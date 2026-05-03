"""
Dialog Windows - StudentDialog dan GradeDialog
Dialog terpisah untuk tambah/edit data
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QPushButton, 
    QMessageBox, QHBoxLayout, QDoubleSpinBox, QLabel
)
from PySide6.QtCore import Slot
from database import DatabaseManager


class StudentDialog(QDialog):
    """Dialog untuk tambah/edit siswa dengan 5 input field"""
    
    def __init__(self, parent, student_controller, student_id=None):
        super().__init__(parent)
        self.student_controller = student_controller
        self.student_id = student_id
        self.student = None
        
        self.setWindowTitle("Tambah Siswa" if not student_id else "Edit Siswa")
        self.setGeometry(200, 200, 400, 350)
        
        self.setup_ui()
        
        if student_id:
            self.load_student_data()
    
    def setup_ui(self):
        """Setup form dialog dengan 5 field input"""
        layout = QVBoxLayout(self)
        
        form_layout = QFormLayout()
        
        # 5 Input fields (requirement)
        self.nim_input = QLineEdit()
        self.name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.address_input = QLineEdit()
        
        form_layout.addRow("NIM:", self.nim_input)
        form_layout.addRow("Nama:", self.name_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Nomor Telepon:", self.phone_input)
        form_layout.addRow("Alamat:", self.address_input)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        btn_save = QPushButton("💾 Simpan")
        btn_cancel = QPushButton("❌ Batal")
        
        btn_save.clicked.connect(self.save_student)
        btn_cancel.clicked.connect(self.reject)
        
        button_layout.addWidget(btn_save)
        button_layout.addWidget(btn_cancel)
        layout.addLayout(button_layout)
    
    def load_student_data(self):
        """Load existing student data"""
        self.student = self.student_controller.get_student(self.student_id)
        if self.student:
            self.nim_input.setText(self.student["nim"])
            self.name_input.setText(self.student["name"])
            self.email_input.setText(self.student["email"])
            self.phone_input.setText(self.student["phone"])
            self.address_input.setText(self.student["address"])
    
    @Slot()
    def save_student(self):
        """Save student data"""
        nim = self.nim_input.text().strip()
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        phone = self.phone_input.text().strip()
        address = self.address_input.text().strip()
        
        # Validation
        if not all([nim, name, email, phone, address]):
            QMessageBox.warning(self, "⚠️ Validasi", "Semua field harus diisi!")
            return
        
        if "@" not in email:
            QMessageBox.warning(self, "⚠️ Validasi", "Email tidak valid!")
            return
        
        if self.student_id:
            # Update
            if self.student_controller.update_student(self.student_id, nim, name, email, phone, address):
                QMessageBox.information(self, "✅ Sukses", "Siswa berhasil diupdate!")
                self.accept()
            else:
                QMessageBox.critical(self, "❌ Error", "NIM sudah terdaftar atau error lainnya!")
        else:
            # Create
            if self.student_controller.add_student(nim, name, email, phone, address):
                QMessageBox.information(self, "✅ Sukses", "Siswa berhasil ditambahkan!")
                self.accept()
            else:
                QMessageBox.critical(self, "❌ Error", "NIM sudah terdaftar atau error lainnya!")


class GradeDialog(QDialog):
    """Dialog untuk tambah/edit nilai dengan 5 input field"""
    
    def __init__(self, parent, grade_controller, students, grade_id=None):
        super().__init__(parent)
        self.grade_controller = grade_controller
        self.students = students
        self.grade_id = grade_id
        self.db = DatabaseManager()
        self.grade_data = None
        
        self.setWindowTitle("Tambah Nilai" if not grade_id else "Edit Nilai")
        self.setGeometry(200, 200, 500, 450)
        
        self.setup_ui()
        
        if grade_id:
            self.load_grade_data()
    
    def setup_ui(self):
        """Setup form dialog dengan 5 input fields"""
        layout = QVBoxLayout(self)
        
        form_layout = QFormLayout()
        
        # 5 Input fields (requirement)
        # Field 1: Student selection
        self.student_combo = QComboBox()
        for student in self.students:
            self.student_combo.addItem(f"{student['name']} ({student['nim']})", student['id'])
        form_layout.addRow("Siswa:", self.student_combo)
        
        # Field 2: Subject
        self.subject_input = QLineEdit()
        form_layout.addRow("Mata Pelajaran:", self.subject_input)
        
        # Field 3: Midterm
        self.midterm_input = QDoubleSpinBox()
        self.midterm_input.setRange(0, 100)
        self.midterm_input.setDecimals(2)
        form_layout.addRow("Nilai UTS (30%):", self.midterm_input)
        
        # Field 4: Final
        self.final_input = QDoubleSpinBox()
        self.final_input.setRange(0, 100)
        self.final_input.setDecimals(2)
        form_layout.addRow("Nilai UAS (50%):", self.final_input)
        
        # Field 5: Assignment
        self.assignment_input = QDoubleSpinBox()
        self.assignment_input.setRange(0, 100)
        self.assignment_input.setDecimals(2)
        form_layout.addRow("Nilai Tugas (20%):", self.assignment_input)
        
        # Display calculated total (read-only)
        self.total_label = QLabel("0.00")
        form_layout.addRow("Total Nilai:", self.total_label)
        
        self.grade_label = QLabel("-")
        form_layout.addRow("Grade:", self.grade_label)
        
        layout.addLayout(form_layout)
        
        # Connect signals to update total
        self.midterm_input.valueChanged.connect(self.update_total)
        self.final_input.valueChanged.connect(self.update_total)
        self.assignment_input.valueChanged.connect(self.update_total)
        
        # Buttons
        button_layout = QHBoxLayout()
        btn_save = QPushButton("💾 Simpan")
        btn_cancel = QPushButton("❌ Batal")
        
        btn_save.clicked.connect(self.save_grade)
        btn_cancel.clicked.connect(self.reject)
        
        button_layout.addWidget(btn_save)
        button_layout.addWidget(btn_cancel)
        layout.addLayout(button_layout)
    
    @Slot()
    def update_total(self):
        """Update total and grade based on input values - menggunakan SIGNAL"""
        midterm = self.midterm_input.value()
        final = self.final_input.value()
        assignment = self.assignment_input.value()
        
        total = (midterm * 0.3 + final * 0.5 + assignment * 0.2)
        grade_letter = DatabaseManager.calculate_grade_letter(total)
        
        self.total_label.setText(f"{total:.2f}")
        self.grade_label.setText(grade_letter)
    
    def load_grade_data(self):
        """Load existing grade data"""
        query = "SELECT * FROM grades WHERE id = ?"
        result = self.db.execute_query(query, (self.grade_id,))
        if result:
            self.grade_data = result[0]
            
            # Set values
            index = self.student_combo.findData(self.grade_data["student_id"])
            self.student_combo.setCurrentIndex(index)
            self.subject_input.setText(self.grade_data["subject"])
            self.midterm_input.setValue(self.grade_data["midterm"])
            self.final_input.setValue(self.grade_data["final"])
            self.assignment_input.setValue(self.grade_data["assignment"])
            
            self.update_total()
    
    @Slot()
    def save_grade(self):
        """Save grade data"""
        student_id = self.student_combo.currentData()
        subject = self.subject_input.text().strip()
        midterm = self.midterm_input.value()
        final = self.final_input.value()
        assignment = self.assignment_input.value()
        
        # Validation
        if not subject:
            QMessageBox.warning(self, "⚠️ Validasi", "Mata pelajaran harus diisi!")
            return
        
        if self.grade_id:
            # Update
            if self.grade_controller.update_grade(self.grade_id, subject, midterm, final, assignment):
                QMessageBox.information(self, "✅ Sukses", "Nilai berhasil diupdate!")
                self.accept()
            else:
                QMessageBox.critical(self, "❌ Error", "Gagal mengupdate nilai!")
        else:
            # Create
            if self.grade_controller.add_grade(student_id, subject, midterm, final, assignment):
                QMessageBox.information(self, "✅ Sukses", "Nilai berhasil ditambahkan!")
                self.accept()
            else:
                QMessageBox.critical(self, "❌ Error", "Gagal menambahkan nilai!")
