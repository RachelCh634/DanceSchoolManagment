import flet as ft
from components.modern_card import ModernCard
from components.clean_button import CleanButton
from components.modern_dialog import ModernDialog


class PaymentsView:
    """View for managing student payments"""
    
    def __init__(self, parent, student):
        self.parent = parent
        self.page = parent.page
        self.student = student
        self.dialog = ModernDialog(self.page)

    def render(self):
        """Render payments view"""
        self.parent.clear_layout()
        
        header = self._create_header()
        self.parent.layout.controls.append(header)
        
        payments = self.student.get('payments', [])
        
        if not payments:
            self._render_empty_state()
        else:
            self._render_payments_list(payments)
        
        actions = self._create_actions()
        self.parent.layout.controls.append(actions)
        
        self.page.update()

    def _create_header(self):
        """Create payments header"""
        return ft.Container(
            content=ft.Row([
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    icon_color=ft.Colors.GREY_600,
                    on_click=lambda e: self.parent.show_students(),
                    tooltip="חזרה"
                ),
                ft.Text(
                    f"תשלומים - {self.student['name']}",
                    size=20,
                    weight=ft.FontWeight.W_600,
                    color=ft.Colors.GREY_800
                )
            ], spacing=8),
            padding=ft.padding.symmetric(vertical=16)
        )

    def _render_empty_state(self):
        """Render empty state"""
        empty_state = ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.RECEIPT_LONG_OUTLINED, size=48, color=ft.Colors.GREY_400),
                ft.Text(
                    "אין תשלומים רשומים",
                    size=16,
                    color=ft.Colors.GREY_600,
                    text_align=ft.TextAlign.CENTER
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12),
            padding=ft.padding.all(48),
            alignment=ft.alignment.center
        )
        self.parent.layout.controls.append(empty_state)

    def _render_payments_list(self, payments):
        """Render payments list"""
        total_paid = sum(
            float(p['amount']) for p in payments
            if p['amount'].replace('.', '', 1).isdigit()
        )
        
        summary = ModernCard(
            content=ft.Container(
                content=ft.Row([
                    ft.Text(f"{len(payments)} תשלומים", size=14, color=ft.Colors.GREY_600),
                    ft.Text(f"{total_paid:,.0f}₪", size=18, weight=ft.FontWeight.W_600, color=ft.Colors.GREEN_600)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=ft.padding.all(16)
            )
        )
        self.parent.layout.controls.append(summary)
        
        # Payments list
        payments_list = ft.Column(spacing=8)
        
        for payment in payments:
            payment_item = self._create_payment_item(payment)
            payments_list.controls.append(payment_item)
        
        self.parent.layout.controls.append(payments_list)

    def _create_payment_item(self, payment):
        """Create payment item card"""
        return ModernCard(
            content=ft.Container(
                content=ft.Row([
                    ft.Column([
                        ft.Text(
                            f"{payment['amount']}₪",
                            size=16,
                            weight=ft.FontWeight.W_600,
                            color=ft.Colors.GREY_800
                        ),
                        ft.Text(
                            payment['date'],
                            size=12,
                            color=ft.Colors.GREY_600
                        )
                    ], spacing=2),
                    ft.Text(
                        f"צ'ק #{payment['check_number']}" if payment['payment_method'] == 'צ\'ק' and payment.get('check_number') else payment['payment_method'],
                        size=12,
                        color=ft.Colors.BLUE_600
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=ft.padding.all(12)
            )
        )

    def _create_actions(self):
        """Create action buttons"""
        return ft.Container(
            content=ft.Row([
                CleanButton.create(
                    "הוסף תשלום",
                    ft.Icons.ADD,
                    ft.Colors.BLUE_600,
                    lambda e: self.parent.show_add_payment_form(self.student)
                ),
                CleanButton.create(
                    "חזרה",
                    ft.Icons.ARROW_BACK,
                    ft.Colors.GREY_600,
                    lambda e: self.parent.show_students(),
                    variant="outlined"
                )
            ], spacing=16, alignment=ft.MainAxisAlignment.CENTER),
            padding=ft.padding.symmetric(vertical=24)
        )
