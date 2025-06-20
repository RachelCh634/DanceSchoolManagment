import flet as ft
from components.modern_dialog import ModernDialog
from components.form_fields import FormFields

from views.add_student_view import AddStudentView

from utils.students_data_manager import StudentsDataManager


class AddStudentPage:
    def __init__(self, page, navigation_callback, group_name):
        self.page = page
        self.navigation_callback = navigation_callback
        self.group_name = group_name

        # Managers and helpers
        self.dialog = ModernDialog(page)
        self.data_manager = StudentsDataManager()
        self.view = AddStudentView(self)

        # Main layout
        self.layout = ft.Column(
            spacing=24,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            animate_opacity=300,
        )

        # Form fields
        self.create_form_fields()

        self.show_add_student_form()


    def get_view(self):
        return ft.Container(
            content=self.layout,
            bgcolor=ft.Colors.WHITE,
            padding=ft.padding.all(32),
            expand=True
        )

    def create_form_fields(self):
        """Create all form input fields using FormFields factory"""
        self.name_input = FormFields.create_text_field(
            "שם התלמידה", "הכנסי שם מלא", ft.Icons.PERSON
        )

        self.id_input = FormFields.create_text_field(
            "תעודת זהות", "הכנסי מספר תעודת זהות",
            ft.Icons.BADGE, ft.KeyboardType.NUMBER
        )

        self.phone_input = FormFields.create_text_field(
            "מספר טלפון", "הכנסי מספר טלפון",
            ft.Icons.PHONE, ft.KeyboardType.PHONE
        )

        self.payment_status_dropdown = FormFields.create_dropdown(
            "סטטוס תשלום", ft.Icons.PAYMENT,
            ["חוב", "יתרת זכות", "שולם"], "חוב"
        )

        self.join_date_input = FormFields.create_date_field(
            "תאריך הצטרפות", ft.Icons.CALENDAR_TODAY
        )

        self.group_dropdown = FormFields.create_dropdown(
            "קבוצה", ft.Icons.GROUP, []
        )

        self.has_sister_checkbox = ft.Checkbox(label="יש לה אחות בחוג", value=False)

        self.load_groups()

    def load_groups(self):
        """Load groups and populate dropdown"""
        groups = self.data_manager.load_groups()
        group_names = [group["name"] for group in groups]

        self.group_dropdown.options = [ft.dropdown.Option(name) for name in group_names]

        if self.group_name:
            self.group_dropdown.value = self.group_name

    def show_add_student_form(self):
        """Show the add student form"""
        self.clear_layout()
        self.view.render()

    def add_student(self, e=None):
        """Add new student with validation"""
        form_data = self.get_form_data()

        if not self.validate_form(form_data):
            return

        if self.data_manager.student_exists_in_this_group(form_data["id"], form_data["group"]):
            self.dialog.show_error(f"תלמידה עם ת.ז. {form_data['id']} כבר קיימת במערכת")
            return

        if self.data_manager.add_student(form_data):
            self.dialog.show_success(
                "התלמידה נוספה בהצלחה למערכת!",
                callback=self.go_back
            )
        else:
            self.dialog.show_error("שגיאה בשמירת התלמידה")

    def get_form_data(self):
        """Get data from form fields"""
        return {
            "id": self.id_input.value.strip() if self.id_input.value else "",
            "name": self.name_input.value.strip() if self.name_input.value else "",
            "phone": self.phone_input.value.strip() if self.phone_input.value else "",
            "group": self.group_dropdown.value if self.group_dropdown.value else "",
            "payment_status": self.payment_status_dropdown.value if self.payment_status_dropdown.value else "",
            "join_date": self.join_date_input.value.strip() if self.join_date_input.value else "",
            "has_sister": self.has_sister_checkbox.value if self.payment_status_dropdown.value else "",
            "payments": []
        }

    def validate_form(self, form_data):
        """Validate form data"""
        # Check all fields are filled
        required_fields = ["id", "name", "phone", "group", "payment_status", "join_date"]
        if not all(form_data.get(field) for field in required_fields):
            self.dialog.show_error("יש למלא את כל השדות הנדרשים")
            return False

        # Validate ID format
        if not form_data["id"].isdigit() or len(form_data["id"]) != 9:
            self.dialog.show_error("מספר תעודת זהות חייב להכיל 9 ספרות בלבד")
            return False

        return True

    def go_back(self, e=None):
        """Navigate back to students page"""
        from pages.students_page import StudentsPage
        students_page = StudentsPage(self.page, self.navigation_callback, self.group_name)
        self.navigation_callback(students_page)

    def clear_layout(self):
        """Clear the layout"""
        self.layout.controls.clear()
