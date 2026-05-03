"""
Business Logic Controllers - StudentController dan GradeController
Mengelola logika bisnis aplikasi
"""

from database import DatabaseManager
from typing import List, Optional, Dict


class StudentController:
    """Controller untuk mengelola Student"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def add_student(self, nim: str, name: str, email: str, phone: str, address: str) -> bool:
        if self.db.student_exists(nim):
            return False
        return self.db.add_student(nim, name, email, phone, address)
    
    def get_all_students(self) -> List[Dict]:
        return self.db.get_all_students()
    
    def get_student(self, student_id: int) -> Optional[Dict]:
        return self.db.get_student(student_id)
    
    def update_student(self, student_id: int, nim: str, name: str, email: str, phone: str, address: str) -> bool:
        if self.db.student_exists(nim, exclude_id=student_id):
            return False
        return self.db.update_student(student_id, nim, name, email, phone, address)
    
    def delete_student(self, student_id: int) -> bool:
        return self.db.delete_student(student_id)


class GradeController:
    """Controller untuk mengelola Grade"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def add_grade(self, student_id: int, subject: str, midterm: float, final: float, assignment: float) -> bool:
        return self.db.add_grade(student_id, subject, midterm, final, assignment)
    
    def get_all_grades(self) -> List[Dict]:
        return self.db.get_all_grades()
    
    def get_student_grades(self, student_id: int) -> List[Dict]:
        return self.db.get_student_grades(student_id)
    
    def update_grade(self, grade_id: int, subject: str, midterm: float, final: float, assignment: float) -> bool:
        return self.db.update_grade(grade_id, subject, midterm, final, assignment)
    
    def delete_grade(self, grade_id: int) -> bool:
        return self.db.delete_grade(grade_id)
