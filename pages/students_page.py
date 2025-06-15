import flet as ft
from pages.add_student_page import AddStudentPage
from utils.students_data_manager import StudentsDataManager
from views.students_group_view import StudentsGroupView
from views.student_edit_view import StudentEditView
from views.payments_view import PaymentsView
from views.add_payment_view import AddPaymentView
from components.modern_dialog import ModernDialog


class StudentsPage:
    """Main students page controller"""
    
    def __init__(self, page, navigation_callback, group_name):
        self.page = page
        self.navigation_callback = navigation_callback
        self.group_name = group_name
        
        # Data manager
        self.data_manager = StudentsDataManager()
        
        # Dialog helper
        self.dialog = ModernDialog(page)
        
        # Main layout
        self.layout = ft.Column(
            spacing=24,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            animate_opacity=300,
        )
        
        # Initialize with students list
        self.show_students()

    def get_view(self):
        """Get the main view container"""
        return ft.Container(
            content=self.layout,
            padding=ft.padding.all(24),
            expand=True,
            bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.GREY_50)
        )

    def show_students(self):
        """Show students list view"""
        self.clear_layout()
        students_view = StudentsGroupView(self)
        students_view.render()

    def edit_student(self, student):
        """Show edit student view"""
        edit_view = StudentEditView(self, student)
        edit_view.render()

    def show_payments(self, student):
        """Show payments view"""
        payments_view = PaymentsView(self, student)
        payments_view.render()

    def show_add_payment_form(self, student):
        """Show add payment form"""
        add_payment_view = AddPaymentView(self, student)
        add_payment_view.render()

    def delete_student(self, student_name):
        """Delete student with confirmation"""
        print(f"delete_student called with: {student_name}")
        
        def confirm_delete():
            print(f"Confirming delete for: {student_name}")
            success = self.data_manager.delete_student(student_name)
            
            if success:
                print("Delete successful")
                self.dialog.show_success(
                    f"{student_name} נמחקה",
                    callback=self.show_students
                )
            else:
                print("Delete failed")
                self.dialog.show_error("שגיאה במחיקת התלמידה")
        
        print("Showing confirmation dialog")
        self.dialog.show_confirmation(
            f"האם למחוק את '{student_name}'?",
            "פעולה זו לא ניתנת לביטול",
            confirm_delete
        )


    def _perform_delete(self, student_name):
        """Perform the actual deletion"""
        success = self.data_manager.delete_student(student_name)
        
        if success:
            self.dialog.show_success(
                f"{student_name} נמחקה",
                callback=self.show_students
            )
        else:
            self.dialog.show_error("שגיאה במחיקת התלמידה")

    def go_back(self, e=None):
        """Navigate back to groups page"""
        self.navigation_callback(None, 1)

    def go_to_add_student_page(self, e=None):
        """Navigate to add student page"""
        add_page = AddStudentPage(self.page, self.navigation_callback, self.group_name)
        self.navigation_callback(add_page)

    def clear_layout(self):
        """Clear the layout"""
        self.layout.controls.clear()
