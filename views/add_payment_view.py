import flet as ft
from components.modern_card import ModernCard
from components.clean_button import CleanButton
from components.modern_dialog import ModernDialog


class AddPaymentView:
    """View for adding new payment"""
    
    def __init__(self, parent, student):
        self.parent = parent
        self.page = parent.page
        self.student = student
        self.dialog = ModernDialog(self.page)
        
        # Form fields
        self.amount_input = None
        self.date_input = None
        self.payment_method_dropdown = None

    def render(self):
        """Render add payment form"""
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
        """Create add payment header"""
        return ft.Container(
            content=ft.Row([
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    icon_color=ft.Colors.GREY_600,
                    on_click=lambda e: self.parent.show_payments(self.student),
                    tooltip="חזרה"
                ),
                ft.Text(
                    f"תשלום חדש - {self.student['name']}",
                    size=20,
                    weight=ft.FontWeight.W_600,
                    color=ft.Colors.GREY_800
                )
            ], spacing=8),
            padding=ft.padding.symmetric(vertical=16)
        )

    def _create_form(self):
        """Create payment form"""
        self.amount_input = ft.TextField(
            label="סכום (₪)",
            border_radius=8,
            content_padding=ft.padding.symmetric(horizontal=12, vertical=12),
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        self.date_input = ft.TextField(
            label="תאריך",
            border_radius=8,
            content_padding=ft.padding.symmetric(horizontal=12, vertical=12)
        )
        
        self.payment_method_dropdown = ft.Dropdown(
            label="אופן תשלום",
            border_radius=8,
            content_padding=ft.padding.symmetric(horizontal=12, vertical=12),
            options=[
                ft.dropdown.Option("מזומן"),
                ft.dropdown.Option("אשראי"),
                ft.dropdown.Option("העברה"),
                ft.dropdown.Option("ביט")
            ]
        )
        
        return ModernCard(
            content=ft.Container(
                content=ft.Column([
                    self.amount_input,
                    self.date_input,
                    self.payment_method_dropdown
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
                    self._save_payment
                ),
                CleanButton.create(
                    "ביטול",
                    ft.Icons.CLOSE,
                    ft.Colors.GREY_600,
                    lambda e: self.parent.show_payments(self.student),
                    variant="outlined"
                )
            ], spacing=16, alignment=ft.MainAxisAlignment.CENTER),
            padding=ft.padding.symmetric(vertical=24)
        )

    def _save_payment(self, e):
        """Save new payment"""
        payment_data = {
            "amount": self.amount_input.value.strip() if self.amount_input.value else "",
            "date": self.date_input.value.strip() if self.date_input.value else "",
            "payment_method": self.payment_method_dropdown.value if self.payment_method_dropdown.value else ""
        }
        
        if not all(payment_data.values()):
            self.dialog.show_error("יש למלא את כל השדות הנדרשים")
            return

        # Validate amount is numeric
        try:
            float(payment_data['amount'])
        except ValueError:
            self.dialog.show_error("יש להזין סכום תקין (מספר בלבד)")
            return

        success = self.parent.data_manager.add_payment(self.student['name'], payment_data)
        
        if success:
            self.dialog.show_success(
                "התשלום נשמר בהצלחה!",
                callback=lambda: self.parent.show_payments(self.student)
            )
        else:
            self.dialog.show_error("שגיאה בשמירת התשלום")
