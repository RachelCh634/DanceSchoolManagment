import flet as ft
from components.modern_card import ModernCard
from components.clean_button import CleanButton
from components.modern_dialog import ModernDialog
from utils.validation import ValidationUtils
from utils.date_utils import DateUtils


class StudentEditView:
    """View for editing student information"""
    
    def __init__(self, parent, student):
        self.parent = parent
        self.page = parent.page
        self.student = student
        self.dialog = ModernDialog(self.page)
        
        # Form fields
        self.name_field = None
        self.phone_field = None
        self.group_field = None
        self.payment_field = None
        self.join_date_field = None

    def render(self):
        """Render the edit form"""
        self.parent.clear_layout()
        
        # Header
        header = self._create_header()
        self.parent.layout.controls.append(header)
        
        # Form
        form = self._create_form()
        self.parent.layout.controls.append(form)
        
        # Actions
        actions = self._create_actions()
        self.parent.layout.controls.append(actions)
        
        self.page.update()

    def _create_header(self):
        """Create edit form header"""
        return ft.Container(
            content=ft.Row([
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    icon_color=ft.Colors.GREY_600,
                    on_click=lambda e: self.parent.show_students(),
                    tooltip="חזרה"
                ),
                ft.Text(
                    f"עריכת {self.student['name']}",
                    size=20,
                    weight=ft.FontWeight.W_600,
                    color=ft.Colors.GREY_800
                )
            ], spacing=8),
            padding=ft.padding.symmetric(vertical=16)
        )

    def _create_form(self):
        """Create form fields"""
        self.name_field = ft.TextField(
            value=self.student['name'],
            label="שם מלא",
            border_radius=8,
            content_padding=ft.padding.symmetric(horizontal=12, vertical=12)
        )
        
        self.phone_field = ft.TextField(
            value=self.student['phone'],
            label="טלפון",
            border_radius=8,
            content_padding=ft.padding.symmetric(horizontal=12, vertical=12)
        )
        
        self.group_field = ft.TextField(
            value=self.student['group'],
            label="קבוצה",
            border_radius=8,
            content_padding=ft.padding.symmetric(horizontal=12, vertical=12)
        )
        
        self.payment_field = ft.TextField(
            value=self.student['payment_status'],
            label="סטטוס תשלום",
            border_radius=8,
            content_padding=ft.padding.symmetric(horizontal=12, vertical=12)
        )
        
        self.join_date_field = ft.TextField(
            value=self.student['join_date'],
            label="תאריך הצטרפות (dd/mm/yyyy)",
            border_radius=8,
            content_padding=ft.padding.symmetric(horizontal=12, vertical=12)
        )
        
        return ModernCard(
            content=ft.Container(
                content=ft.Column([
                    self.name_field,
                    self.phone_field,
                    self.group_field,
                    self.payment_field,
                    self.join_date_field
                ], spacing=16),
                padding=ft.padding.all(20)
            )
        )

    def _create_actions(self):
        """Create action buttons"""
        return ft.Container(
            content=ft.Row([
                CleanButton.create(
                    "שמור",
                    ft.Icons.CHECK,
                    ft.Colors.GREEN_600,
                    self._save_student
                ),
                CleanButton.create(
                    "ביטול",
                    ft.Icons.CLOSE,
                    ft.Colors.GREY_600,
                    lambda e: self.parent.show_students(),
                    variant="outlined"
                )
            ], spacing=16, alignment=ft.MainAxisAlignment.CENTER),
            padding=ft.padding.symmetric(vertical=24)
        )

    def _save_student(self, e):
        """Save student changes with validation"""
        # Get form data
        form_data = {
            "name": self.name_field.value.strip() if self.name_field.value else "",
            "phone": self.phone_field.value.strip() if self.phone_field.value else "",
            "group": self.group_field.value.strip() if self.group_field.value else "",
            "payment_status": self.payment_field.value.strip() if self.payment_field.value else "",
            "join_date": self.join_date_field.value.strip() if self.join_date_field.value else ""
        }
        
        # Validate required fields
        is_valid, empty_fields = ValidationUtils.validate_required_fields(form_data)
        if not is_valid:
            self.dialog.show_error("יש למלא את כל השדות הנדרשים")
            return
        
        # Validate name
        name_valid, name_error = ValidationUtils.validate_name(form_data["name"])
        if not name_valid:
            self.dialog.show_error(name_error)
            return
        
        # Validate phone
        phone_valid, phone_error = ValidationUtils.validate_phone(form_data["phone"])
        if not phone_valid:
            self.dialog.show_error(phone_error)
            return
        
        # Validate date
        date_valid, date_error = DateUtils.validate_date(form_data["join_date"])
        if not date_valid:
            self.dialog.show_error(date_error)
            return
        
        # Create updated student data
        new_data = {
            "id": self.student.get('id', ''),
            "name": form_data["name"],
            "phone": form_data["phone"],
            "group": form_data["group"],
            "payment_status": form_data["payment_status"],
            "join_date": DateUtils.format_date(form_data["join_date"]),
            "payments": self.student.get('payments', [])
        }
        
        # Save to data manager
        success = self.parent.data_manager.update_student(self.student['name'], new_data)
        
        if success:
            self.dialog.show_success(
                "התלמידה נשמרה בהצלחה",
                callback=self.parent.show_students
            )
        else:
            self.dialog.show_error("שגיאה בשמירת התלמידה")
