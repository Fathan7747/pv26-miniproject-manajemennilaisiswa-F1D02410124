"""
Database Management - SQLite Operations
"""

import sqlite3
import os
from typing import List, Dict, Tuple, Optional

class DatabaseManager:
    def __init__(self, db_name="students_grades.db"):
        self.db_path = db_name
        print(f"📂 Database path: {os.path.abspath(self.db_path)}")
        self.init_database()
        print("✅ Database initialized successfully!")
    
    def init_database(self):
        """Initialize database dan buat tabel jika belum ada"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # tabel students 
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='students'
            """)
            students_exists = cursor.fetchone() is not None
            
            # tabel grades 
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='grades'
            """)
            grades_exists = cursor.fetchone() is not None
            
            # Buat tabel students 
            if not students_exists:
                print("📝 Creating students table...")
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS students (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nim TEXT UNIQUE NOT NULL,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        phone TEXT NOT NULL,
                        address TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                print("✅ Students table created!")
            
            # Buat tabel grades 
            if not grades_exists:
                print("📝 Creating grades table...")
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS grades (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        student_id INTEGER NOT NULL,
                        subject TEXT NOT NULL,
                        midterm REAL NOT NULL,
                        final REAL NOT NULL,
                        assignment REAL NOT NULL,
                        total REAL NOT NULL,
                        grade_letter TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (student_id) REFERENCES students(id)
                    )
                ''')
                print("✅ Grades table created!")
            
            conn.commit()
            conn.close()
            
        except sqlite3.Error as e:
            print(f"❌ Database initialization error: {e}")
            raise
    
    def execute_query(self, query: str, params: Tuple = ()) -> List[Dict]:
        """Execute SELECT query"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params)
            result = [dict(row) for row in cursor.fetchall()]
            conn.close()
            return result
        except sqlite3.Error as e:
            print(f"❌ Database query error: {e}")
            return []
    
    def execute_update(self, query: str, params: Tuple = ()) -> bool:
        """Execute INSERT/UPDATE/DELETE query"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"❌ Database update error: {e}")
            return False
    
    def get_last_id(self) -> int:
        """Get last inserted ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT last_insert_rowid()")
            result = cursor.fetchone()[0]
            conn.close()
            return result
        except sqlite3.Error as e:
            print(f"❌ Database error: {e}")
            return -1

    # ===== STUDENT OPERATIONS =====
    def add_student(self, nim: str, name: str, email: str, phone: str, address: str) -> bool:
        """Tambah siswa baru"""
        query = "INSERT INTO students (nim, name, email, phone, address) VALUES (?, ?, ?, ?, ?)"
        return self.execute_update(query, (nim, name, email, phone, address))
    
    def get_all_students(self) -> List[Dict]:
        """Ambil semua siswa"""
        query = "SELECT * FROM students ORDER BY name ASC"
        return self.execute_query(query)
    
    def get_student(self, student_id: int) -> Optional[Dict]:
        """Ambil siswa berdasarkan ID"""
        query = "SELECT * FROM students WHERE id = ?"
        result = self.execute_query(query, (student_id,))
        return result[0] if result else None
    
    def update_student(self, student_id: int, nim: str, name: str, email: str, phone: str, address: str) -> bool:
        """Update siswa"""
        query = "UPDATE students SET nim=?, name=?, email=?, phone=?, address=? WHERE id=?"
        return self.execute_update(query, (nim, name, email, phone, address, student_id))
    
    def delete_student(self, student_id: int) -> bool:
        """Hapus siswa dan nilai-nilainya"""
        # Delete related grades first
        query_grades = "DELETE FROM grades WHERE student_id=?"
        self.execute_update(query_grades, (student_id,))
        
        # Delete student
        query = "DELETE FROM students WHERE id=?"
        return self.execute_update(query, (student_id,))
    
    def student_exists(self, nim: str, exclude_id: int = None) -> bool:
        """Cek apakah NIM sudah terdaftar"""
        if exclude_id:
            query = "SELECT COUNT(*) as count FROM students WHERE nim=? AND id!=?"
            result = self.execute_query(query, (nim, exclude_id))
        else:
            query = "SELECT COUNT(*) as count FROM students WHERE nim=?"
            result = self.execute_query(query, (nim,))
        
        if result:
            return result[0]['count'] > 0
        return False

    # ===== GRADE OPERATIONS =====
    def add_grade(self, student_id: int, subject: str, midterm: float, final: float, assignment: float) -> bool:
        """Tambah nilai baru"""
        total = (midterm * 0.3 + final * 0.5 + assignment * 0.2)
        grade_letter = self.calculate_grade_letter(total)
        query = "INSERT INTO grades (student_id, subject, midterm, final, assignment, total, grade_letter) VALUES (?, ?, ?, ?, ?, ?, ?)"
        return self.execute_update(query, (student_id, subject, midterm, final, assignment, total, grade_letter))
    
    def get_all_grades(self) -> List[Dict]:
        """Ambil semua nilai dengan info siswa"""
        query = """SELECT g.*, s.name, s.nim FROM grades g 
                   JOIN students s ON g.student_id = s.id 
                   ORDER BY s.name ASC"""
        return self.execute_query(query)
    
    def get_student_grades(self, student_id: int) -> List[Dict]:
        """Ambil semua nilai siswa"""
        query = "SELECT * FROM grades WHERE student_id=? ORDER BY subject ASC"
        return self.execute_query(query, (student_id,))
    
    def get_grade(self, grade_id: int) -> Optional[Dict]:
        """Ambil nilai berdasarkan ID"""
        query = "SELECT * FROM grades WHERE id = ?"
        result = self.execute_query(query, (grade_id,))
        return result[0] if result else None
    
    def update_grade(self, grade_id: int, subject: str, midterm: float, final: float, assignment: float) -> bool:
        """Update nilai"""
        total = (midterm * 0.3 + final * 0.5 + assignment * 0.2)
        grade_letter = self.calculate_grade_letter(total)
        query = "UPDATE grades SET subject=?, midterm=?, final=?, assignment=?, total=?, grade_letter=? WHERE id=?"
        return self.execute_update(query, (subject, midterm, final, assignment, total, grade_letter, grade_id))
    
    def delete_grade(self, grade_id: int) -> bool:
        """Hapus nilai"""
        query = "DELETE FROM grades WHERE id=?"
        return self.execute_update(query, (grade_id,))
    
    @staticmethod
    def calculate_grade_letter(total: float) -> str:
        """Hitung grade letter dari total nilai"""
        if total >= 85:
            return "A"
        elif total >= 75:
            return "B"
        elif total >= 65:
            return "C"
        elif total >= 55:
            return "D"
        else:
            return "E"