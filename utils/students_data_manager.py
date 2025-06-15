import json
import os
from typing import List, Dict, Any


class StudentsDataManager:
    """Manager for students data operations"""
    
    def __init__(self):
        self.students_file = "data/students.json"
        self.groups_file = "data/groups.json"

    def load_students(self):
        """Load students from JSON file"""
        try:
            with open(self.students_file, encoding="utf-8") as f:
                data = json.load(f)
                return data.get("students", [])
        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"Error loading students: {e}")
            return []
        
    def get_students_stats(self, students: List[Dict[str, Any]]) -> Dict[str, int]:
        """Calculate students statistics"""
        total_students = len(students)
        paid_students = len([s for s in students if s.get("payment_status") == "שולם"])
        unpaid_students = total_students - paid_students
        
        return {
            "total": total_students,
            "paid": paid_students,
            "unpaid": unpaid_students
        }
    
    def filter_students(self, students: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        """Filter students based on search query"""
        if not query:
            return students.copy()
        
        query_lower = query.lower()
        return [
            student for student in students
            if query_lower in json.dumps(student, ensure_ascii=False).lower()
        ]


    def get_all_students(self):
        """Get all students"""
        try:
            with open(self.students_file, encoding="utf-8") as f:
                return json.load(f).get("students", [])
        except Exception as e:
            print(f"Error loading students: {e}")
            return []

    def get_students_by_group(self, group_name):
        """Get students filtered by group"""
        students = self.get_all_students()
        return [s for s in students if s.get("group") == group_name]

    def save_students(self, students):
        """Save students to file"""
        try:
            with open(self.students_file, 'w', encoding="utf-8") as f:
                json.dump({"students": students}, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"Error saving students: {e}")
            return False

    def load_groups(self):
        """Load groups from JSON file"""
        try:
            with open(self.groups_file, encoding="utf-8") as f:
                data = json.load(f)
                return data.get("groups", [])
        except Exception as e:
            print(f"Error loading groups: {e}")
            return []
        
    def update_student(self, original_name, new_data):
        """Update a specific student"""
        students = self.get_all_students()
        
        for i, student in enumerate(students):
            if student['name'] == original_name:
                students[i] = new_data
                break
        
        return self.save_students(students)

    def add_student(self, student_data):
        """Add new student"""
        students = self.load_students()
        students.append(student_data)
        return self.save_students(students)
    
    def student_exists(self, student_id):
        """Check if student with given ID exists"""
        students = self.load_students()
        return any(student.get("id") == student_id for student in students)
    
    def delete_student(self, student_name):
        """Delete a student"""
        try:
            print(f"Attempting to delete student: {student_name}")  # דיבוג
            
            students = self.get_all_students()
            print(f"Total students before deletion: {len(students)}")  # דיבוג
            
            # מצא את התלמיד לפני המחיקה
            student_exists = any(s['name'] == student_name for s in students)
            print(f"Student exists: {student_exists}")  # דיבוג
            
            updated_students = [s for s in students if s['name'] != student_name]
            print(f"Total students after deletion: {len(updated_students)}")  # דיבוג
            
            success = self.save_students(updated_students)
            print(f"Save successful: {success}")  # דיבוג
            
            return success
            
        except Exception as e:
            print(f"Error in delete_student: {e}")
            return False


    def add_payment(self, student_name, payment_data):
        """Add payment to student and update payment status"""
        students = self.get_all_students()
        groups = self._get_groups()
        
        for student in students:
            if student['name'] == student_name:
                student.setdefault("payments", []).append(payment_data)
                
                # Calculate total paid
                total_paid = sum(
                    float(p['amount']) for p in student['payments']
                    if p['amount'].replace('.', '', 1).isdigit()
                )
                
                group_name = student.get("group")
                group = next((g for g in groups if g['name'] == group_name), None)
                
                if group:
                    group_price = float(group.get("price", "0"))
                    if total_paid >= group_price:
                        student['payment_status'] = "שולם"
                    else:
                        student['payment_status'] = f"חוב: {group_price - total_paid:,.0f}₪"
                else:
                    student['payment_status'] = "לא נמצא מחיר קבוצה"
                break
        
        return self.save_students(students)

    def _get_groups(self):
        """Get groups data for pricing"""
        try:
            with open(self.groups_file, encoding="utf-8") as f:
                return json.load(f).get("groups", [])
        except Exception as e:
            print(f"Error loading groups: {e}")
            return []
