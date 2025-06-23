import flet as ft
from components.modern_card import ModernCard
from components.clean_button import CleanButton
from components.modern_dialog import ModernDialog
from utils.payment_utils import PaymentCalculator
import os
import json

class PaymentsView:
    """View for managing student payments"""
    
    def __init__(self, parent, student):
        self.parent = parent
        self.page = parent.page
        self.student_id = student.get('id') 
        self.student = None  
        self.dialog = ModernDialog(self.page)
        self.payment_calculator = PaymentCalculator()
        self.load_student_data()

    def load_student_data(self):
            """Load fresh student data from file"""
            try:
                if os.path.exists("data/students.json"):
                    with open("data/students.json", "r", encoding="utf-8") as f:
                        students_data = json.load(f)
                        
                    for student in students_data.get("students", []):
                        if student.get("id") == self.student_id:
                            self.student = student
                            break
                    
                    if not self.student:
                        self.student = {"id": self.student_id, "name": "תלמיד לא נמצא", "payments": []}
                else:
                    self.student = {"id": self.student_id, "name": "קובץ לא נמצא", "payments": []}
                    
            except Exception as e:
                self.student = {"id": self.student_id, "name": "שגיאה בטעינה", "payments": []}

    def refresh_student_data(self):
        """Refresh student data from file"""
        self.load_student_data()

    def render(self):
        """Render payments view"""
        self.refresh_student_data()
        
        self.parent.clear_layout()
        
        header = self._create_header()
        self.parent.layout.controls.append(header)
        
        # הוספת הסבר חישוב התשלום
        payment_explanation = self._create_payment_explanation()
        if payment_explanation:
            self.parent.layout.controls.append(payment_explanation)
        
        payments = self.student.get('payments', [])
        
        if not payments:
            self._render_empty_state()
        else:
            self._render_payments_list()
        
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

    def _create_payment_explanation(self):
        """Create payment calculation explanation card"""
        try:
            join_date = self.student.get('join_date', '')
            
            if not join_date:
                print("DEBUG: No join_date found")
                return None
            
            explanation = self.payment_calculator.get_student_payment_explanation(
                self.student_id, join_date
            )
            
            if not explanation.get("success"):
                print(f"DEBUG: explanation failed: {explanation}")
                return None
            
            detailed_summary = explanation.get("summary", "")
            
            if not detailed_summary:
                print("DEBUG: No detailed_summary found")
                return None
            
            return ModernCard(
                content=ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.CALCULATE, size=20, color=ft.Colors.BLUE_600),
                            ft.Text(
                                "הסבר חישוב התשלום",
                                size=16,
                                weight=ft.FontWeight.W_600,
                                color=ft.Colors.GREY_800
                            ),
                            ft.Container(expand=True),
                            ft.IconButton(
                                icon=ft.Icons.INFO_OUTLINE,
                                icon_size=20,
                                icon_color=ft.Colors.BLUE_600,
                                tooltip="פרטים נוספים",
                                on_click=lambda e: self._show_detailed_explanation(explanation)
                            )
                        ], alignment=ft.MainAxisAlignment.START),
                        
                        ft.Container(height=8),
                        
                        # הצגת הסיכום הקצר
                        ft.Container(
                            content=ft.Text(
                                self._create_short_summary(explanation),
                                size=14,
                                color=ft.Colors.GREY_700,
                                selectable=True
                            ),
                            bgcolor=ft.Colors.GREY_50,
                            padding=ft.padding.all(12),
                            border_radius=8,
                            border=ft.border.all(1, ft.Colors.GREY_200)
                        )
                    ], spacing=0),
                    padding=ft.padding.all(16)
                )
            )
            
        except Exception as e:
            print(f"DEBUG: Error creating payment explanation: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _create_short_summary(self, explanation):
        """Create a short summary for the card"""
        try:
            price_breakdown = explanation.get("price_breakdown", {})
            payment_breakdown = explanation.get("payment_breakdown", {})
            payments_made = explanation.get("payments_made", {})
            
            groups = explanation.get("groups", [])
            num_groups = explanation.get("num_groups", 0)
            has_sister = explanation.get("has_sister", False)
            
            final_monthly_price = price_breakdown.get("final_monthly_price", 0)
            total_required = payment_breakdown.get("total_required", 0)
            total_paid = payments_made.get("total_paid", 0)
            balance = payments_made.get("balance", 0)
            
            lines = []
            
            # מחיר חודשי
            price_line = f"מחיר חודשי: {final_monthly_price}₪"
            if num_groups > 1:
                price_line += f" ({num_groups} קבוצות)"
            if has_sister:
                price_line += " (עם הנחת אחיות)"
            lines.append(price_line)
            
            # סה"כ נדרש
            lines.append(f"סה\"כ נדרש עד כה: {total_required}₪")
            
            # שולם
            lines.append(f"שולם: {total_paid}₪")
            
            # יתרה
            if balance > 0:
                lines.append(f"יתרת חוב: {balance}₪ ❌")
            elif balance == 0:
                lines.append("סטטוס: שולם במלואו ✅")
            else:
                lines.append("")
            
            return "\n".join(lines)
            
        except Exception as e:
            return "שגיאה בהצגת סיכום התשלום"

    def _show_detailed_explanation(self, explanation):
        """Show detailed payment explanation in dialog"""
        try:
            summary_text = explanation.get("summary", "")
            
            detailed_dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text(
                    f"הסבר מפורט - {explanation.get('student_name', '')}",
                    size=18,
                    weight=ft.FontWeight.W_600,
                    text_align=ft.TextAlign.RIGHT  
                ),
                content=ft.Container(
                    content=ft.Column([
                        ft.Container(
                            content=ft.Text(
                                summary_text,
                                size=13,
                                selectable=True,
                                color=ft.Colors.GREY_800,
                                text_align=ft.TextAlign.RIGHT  # יישור הטקסט לימין
                            ),
                            bgcolor=ft.Colors.WHITE,
                            padding=ft.padding.all(16),
                            border_radius=8,
                            border=ft.border.all(1, ft.Colors.WHITE)
                        )
                    ], scroll=ft.ScrollMode.AUTO),
                    width=600,
                    height=400
                ),
                actions=[
                    ft.TextButton(
                        "סגור",
                        on_click=lambda e: self._close_dialog(detailed_dialog)
                    )
                ],
                actions_alignment=ft.MainAxisAlignment.END
            )
            
            self.page.open(detailed_dialog)
            self.page.update()
            
        except Exception as e:
            self.dialog.show_error(f"שגיאה בהצגת ההסבר המפורט: {str(e)}")


    def _close_dialog(self, dialog):
        """Close dialog"""
        self.page.close(dialog)
        self.page.update()

    def _render_empty_state(self):
        """Render empty state"""
        payments = self.student.get('payments', [])
        
        if payments:
            self._render_payments_list()
        
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

    def _render_payments_list(self):
        """Render payments list"""
        payments = self.student.get('payments', [])
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
