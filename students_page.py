import json
import flet as ft
from add_student_page import AddStudentPage


class ModernCard(ft.Container):
    def __init__(self, content=None, hover_effect=True, **kwargs):
        super().__init__(
            content=content,
            bgcolor=ft.Colors.WHITE,
            border_radius=16,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=20,
                color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                offset=ft.Offset(0, 8),
            ),
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT) if hover_effect else None,
            **kwargs
        )


class StudentsPage:
    def __init__(self, page, navigation_callback, group_name):
        self.page = page
        self.navigation_callback = navigation_callback
        self.group_name = group_name
        
        # Main layout with modern styling
        self.layout = ft.Column(
            spacing=24,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            animate_opacity=300,
        )
        
        # Store cards for animation
        self.cards = []
        
        self.show_students()

    def get_view(self):
        return ft.Container(
            content=self.layout,
            padding=ft.padding.all(32),
            expand=True
        )

    def create_modern_button(self, text, icon, color, on_click, variant="elevated"):
        """Create a modern button with React-like styling"""
        if variant == "elevated":
            return ft.ElevatedButton(
                content=ft.Row([
                    ft.Icon(icon, size=18, color=ft.Colors.WHITE),
                    ft.Text(text, size=14, weight=ft.FontWeight.W_500, color=ft.Colors.WHITE)
                ], spacing=8, tight=True),
                bgcolor=color,
                color=ft.Colors.WHITE,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=12),
                    padding=ft.padding.symmetric(horizontal=20, vertical=14),
                    elevation={"": 2, "hovered": 8, "pressed": 1},
                    animation_duration=200,
                    bgcolor={
                        "": color,
                        "hovered": ft.Colors.with_opacity(0.9, color),
                        "pressed": ft.Colors.with_opacity(0.8, color)
                    }
                ),
                on_click=on_click
            )
        else:  # outlined variant
            return ft.OutlinedButton(
                content=ft.Row([
                    ft.Icon(icon, size=18, color=color),
                    ft.Text(text, size=14, weight=ft.FontWeight.W_500, color=color)
                ], spacing=8, tight=True),
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=12),
                    padding=ft.padding.symmetric(horizontal=20, vertical=14),
                    side=ft.BorderSide(2, color),
                    bgcolor={
                        "": ft.Colors.TRANSPARENT,
                        "hovered": ft.Colors.with_opacity(0.05, color),
                    }
                ),
                on_click=on_click
            )

    def show_students(self):
        self.clear_layout()
        self.cards = []
        
        # Modern Header with gradient
        header_card = ModernCard(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Container(
                            content=ft.Icon(
                                ft.Icons.GROUPS,
                                size=32,
                                color=ft.Colors.WHITE
                            ),
                            bgcolor=ft.Colors.BLUE,
                            border_radius=50,
                            padding=ft.padding.all(12),
                        ),
                        ft.Column([
                            ft.Text(
                                "רשימת תלמידות",
                                size=28,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.GREY_800,
                            ),
                            ft.Text(
                                f"קבוצת {self.group_name}",
                                size=16,
                                color=ft.Colors.GREY_600,
                                weight=ft.FontWeight.W_400
                            )
                        ], spacing=4, expand=True)
                    ], spacing=16, alignment=ft.MainAxisAlignment.START),
                ], spacing=16),
                padding=ft.padding.all(24)
            ),
            gradient=ft.LinearGradient(
                colors=[ft.Colors.WHITE, ft.Colors.with_opacity(0.98, ft.Colors.BLUE_50)],
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
            )
        )
        
        self.layout.controls.append(header_card)
        
        # Load students data
        try:
            with open("data/students.json", encoding="utf-8") as f:
                students = json.load(f).get("students", [])
        except Exception as e:
            error_card = ModernCard(
                content=ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.ERROR_OUTLINE, size=48, color=ft.Colors.RED_400),
                        ft.Text(
                            "שגיאה בטעינת התלמידות",
                            size=18,
                            weight=ft.FontWeight.W_500,
                            color=ft.Colors.RED_600,
                            text_align=ft.TextAlign.CENTER
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=16),
                    padding=ft.padding.all(32)
                )
            )
            self.layout.controls.append(error_card)
            print("Error:", e)
            students = []

        self.current_students = [s for s in students if s.get("group") == self.group_name]

        # Students Grid/List
        if not self.current_students:
            empty_card = ModernCard(
                content=ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.PERSON_OFF_OUTLINED, size=64, color=ft.Colors.GREY_400),
                        ft.Text(
                            "אין תלמידות בקבוצה זו",
                            size=20,
                            weight=ft.FontWeight.W_500,
                            color=ft.Colors.GREY_600,
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Text(
                            "התחילו בהוספת התלמידה הראשונה",
                            size=14,
                            color=ft.Colors.GREY_500,
                            text_align=ft.TextAlign.CENTER
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12),
                    padding=ft.padding.all(48)
                )
            )
            self.layout.controls.append(empty_card)
        else:
            # Students container with modern grid
            students_container = ModernCard(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(
                            f"סה״כ {len(self.current_students)} תלמידות",
                            size=16,
                            weight=ft.FontWeight.W_500,
                            color=ft.Colors.GREY_700
                        ),
                        ft.Divider(height=1, color=ft.Colors.GREY_300),
                        ft.Container(
                            content=ft.Column([
                                self.create_student_card(student) 
                                for student in self.current_students
                            ], spacing=16, scroll=ft.ScrollMode.AUTO), 
                            padding=ft.padding.symmetric(vertical=16),
                        )
                    ], spacing=16),
                    padding=ft.padding.all(24)
                ),
                hover_effect=False
            )
            self.layout.controls.append(students_container)
        
        # Modern Action Buttons
        actions_card = ModernCard(
            content=ft.Container(
                content=ft.Row([
                    self.create_modern_button(
                        "הוסף תלמידה",
                        ft.Icons.PERSON_ADD,
                        ft.Colors.GREEN_600,
                        self.go_to_add_student_page
                    ),
                    self.create_modern_button(
                        "חזרה לקבוצות",
                        ft.Icons.ARROW_BACK,
                        ft.Colors.GREY_600,
                        self.go_back,
                        variant="outlined"
                    )
                ], spacing=16, alignment=ft.MainAxisAlignment.CENTER),
                padding=ft.padding.all(20)
            )
        )
        
        self.layout.controls.append(actions_card)
        self.page.update()

    def create_student_card(self, student):
        """Create a modern student card with React-like design"""
        
        # Student avatar with modern design
        avatar = ft.Container(
            content=ft.Text(
                student['name'][0] if student['name'] else "?",
                color=ft.Colors.WHITE,
                size=20,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER
            ),
            bgcolor=ft.Colors.BLUE_600,
            border_radius=25,
            width=50,
            height=50,
            alignment=ft.alignment.center,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.3, ft.Colors.BLUE_600),
                offset=ft.Offset(0, 2),
            )
        )
        
        # Payment status chip
        payment_status = student.get('payment_status', '')
        if payment_status == "שולם":
            status_color = ft.Colors.GREEN_600
            status_bg = ft.Colors.GREEN_50
            status_icon = ft.Icons.CHECK_CIRCLE
        elif "חוב" in payment_status:
            status_color = ft.Colors.RED_600
            status_bg = ft.Colors.RED_50
            status_icon = ft.Icons.ERROR
        else:
            status_color = ft.Colors.ORANGE_600
            status_bg = ft.Colors.ORANGE_50
            status_icon = ft.Icons.SCHEDULE
        
        status_chip = ft.Container(
            content=ft.Row([
                ft.Icon(status_icon, size=16, color=status_color),
                ft.Text(
                    payment_status,
                    size=12,
                    weight=ft.FontWeight.W_500,
                    color=status_color
                )
            ], spacing=4, tight=True),
            bgcolor=status_bg,
            border_radius=20,
            padding=ft.padding.symmetric(horizontal=12, vertical=6)
        )
        
        # Student info section
        info_section = ft.Column([
            ft.Row([
                avatar,
                ft.Column([
                    ft.Text(
                        student['name'],
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.GREY_800
                    ),
                    ft.Text(
                        f"הצטרף ב-{student.get('join_date', 'לא ידוע')}",
                        size=12,
                        color=ft.Colors.GREY_500
                    )
                ], spacing=2, expand=True),
                status_chip
            ], spacing=16, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            
            ft.Divider(height=1, color=ft.Colors.GREY_200),
            
            # Contact info with modern icons
            ft.Row([
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.PHONE, size=16, color=ft.Colors.BLUE_600),
                        ft.Text(
                            student.get('phone', 'לא צוין'),
                            size=14,
                            color=ft.Colors.GREY_700
                        )
                    ], spacing=8),
                    expand=True
                ),
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.GROUP, size=16, color=ft.Colors.PURPLE_600),
                        ft.Text(
                            student.get('group', 'לא צוין'),
                            size=14,
                            color=ft.Colors.GREY_700
                        )
                    ], spacing=8),
                    expand=True
                )
            ], spacing=16)
        ], spacing=16)
        
        # Action buttons with modern design
        action_buttons = ft.Row([
            ft.IconButton(
                icon=ft.Icons.EDIT,
                icon_color=ft.Colors.BLUE_600,
                bgcolor=ft.Colors.BLUE_50,
                tooltip="עריכה",
                on_click=lambda e: self.edit_single_student(student),
                style=ft.ButtonStyle(
                    shape=ft.CircleBorder(),
                    padding=ft.padding.all(12)
                )
            ),
            ft.IconButton(
                icon=ft.Icons.PAYMENT,
                icon_color=ft.Colors.PURPLE_600,
                bgcolor=ft.Colors.PURPLE_50,
                tooltip="תשלומים",
                on_click=lambda e: self.show_payments(student),
                style=ft.ButtonStyle(
                    shape=ft.CircleBorder(),
                    padding=ft.padding.all(12)
                )
            ),
            ft.IconButton(
                icon=ft.Icons.DELETE,
                icon_color=ft.Colors.RED_600,
                bgcolor=ft.Colors.RED_50,
                tooltip="מחיקה",
                on_click=lambda e: self.confirm_delete(student['name']),
                style=ft.ButtonStyle(
                    shape=ft.CircleBorder(),
                    padding=ft.padding.all(12)
                )
            )
        ], spacing=8, alignment=ft.MainAxisAlignment.END)
        
        # Main card container
        card = ft.Container(
            content=ft.Column([
                info_section,
                action_buttons
            ], spacing=20),
            bgcolor=ft.Colors.WHITE,
            border_radius=16,
            padding=ft.padding.all(20),
            border=ft.border.all(1, ft.Colors.GREY_200),
        shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.06, ft.Colors.BLACK),
                offset=ft.Offset(0, 4),
            ),
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
            on_hover=self.on_card_hover
        )
        
        return card

    def on_card_hover(self, e):
        """Handle card hover effect"""
        if e.data == "true":
            e.control.shadow = ft.BoxShadow(
                spread_radius=0,
                blur_radius=20,
                color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                offset=ft.Offset(0, 8),
            )
        else:
            e.control.shadow = ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.06, ft.Colors.BLACK),
                offset=ft.Offset(0, 4),
            )
        e.control.update()

    def confirm_delete(self, student_name):
        """Modern delete confirmation dialog"""
        def handle_yes(e):
            self.delete_student(student_name)
            dialog.open = False
            self.page.update()
            
        def handle_no(e):
            dialog.open = False
            self.page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(ft.Icons.WARNING, color=ft.Colors.RED_600, size=24),
                ft.Text("אישור מחיקה", size=20, weight=ft.FontWeight.BOLD)
            ], spacing=12),
            content=ft.Container(
                content=ft.Column([
                    ft.Text(
                        f"האם אתה בטוח שברצונך למחוק את התלמידה '{student_name}'?",
                        size=16,
                        color=ft.Colors.GREY_700
                    ),
                    ft.Text(
                        "פעולה זו לא ניתנת לביטול",
                        size=14,
                        color=ft.Colors.RED_600,
                        weight=ft.FontWeight.W_500
                    )
                ], spacing=8),
                padding=ft.padding.symmetric(vertical=16)
            ),
            actions=[
                ft.TextButton(
                    "ביטול",
                    on_click=handle_no,
                    style=ft.ButtonStyle(
                        color=ft.Colors.GREY_600,
                        padding=ft.padding.symmetric(horizontal=20, vertical=12)
                    )
                ),
                ft.ElevatedButton(
                    "מחק",
                    on_click=handle_yes,
                    bgcolor=ft.Colors.RED_600,
                    color=ft.Colors.WHITE,
                    style=ft.ButtonStyle(
                        padding=ft.padding.symmetric(horizontal=20, vertical=12)
                    )
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            shape=ft.RoundedRectangleBorder(radius=16)
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def edit_single_student(self, student):
        """Modern edit student form"""
        self.clear_layout()
        
        # Header
        header_card = ModernCard(
            content=ft.Container(
                content=ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        icon_color=ft.Colors.GREY_600,
                        on_click=lambda e: self.show_students(),
                        tooltip="חזרה"
                    ),
                    ft.Column([
                        ft.Text(
                            "עריכת תלמידה",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREY_800
                        ),
                        ft.Text(
                            student['name'],
                            size=16,
                            color=ft.Colors.GREY_600
                        )
                    ], spacing=4, expand=True)
                ], spacing=16),
                padding=ft.padding.all(24)
            )
        )
        self.layout.controls.append(header_card)
        
        # Form fields with modern styling
        name_field = ft.TextField(
            value=student['name'],
            label="שם מלא",
            prefix_icon=ft.Icons.PERSON,
            border_radius=12,
            bgcolor=ft.Colors.GREY_50,
            border_color=ft.Colors.GREY_300,
            focused_border_color=ft.Colors.BLUE_600,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=16)
        )
        
        phone_field = ft.TextField(
            value=student['phone'],
            label="מספר טלפון",
            prefix_icon=ft.Icons.PHONE,
            border_radius=12,
            bgcolor=ft.Colors.GREY_50,
            border_color=ft.Colors.GREY_300,
            focused_border_color=ft.Colors.BLUE_600,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=16)
        )
        
        group_field = ft.TextField(
            value=student['group'],
            label="קבוצה",
            prefix_icon=ft.Icons.GROUP,
            border_radius=12,
            bgcolor=ft.Colors.GREY_50,
            border_color=ft.Colors.GREY_300,
            focused_border_color=ft.Colors.BLUE_600,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=16)
        )
        
        payment_field = ft.TextField(
            value=student['payment_status'],
            label="סטטוס תשלום",
            prefix_icon=ft.Icons.PAYMENT,
            border_radius=12,
            bgcolor=ft.Colors.GREY_50,
            border_color=ft.Colors.GREY_300,
            focused_border_color=ft.Colors.BLUE_600,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=16)
        )
        
        join_date_field = ft.TextField(
            value=student['join_date'],
            label="תאריך הצטרפות",
            prefix_icon=ft.Icons.CALENDAR_TODAY,
            border_radius=12,
            bgcolor=ft.Colors.GREY_50,
            border_color=ft.Colors.GREY_300,
            focused_border_color=ft.Colors.BLUE_600,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=16)
        )
        
        # Form card
        form_card = ModernCard(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(
                        "פרטי התלמידה",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.GREY_800
                    ),
                    ft.Divider(height=1, color=ft.Colors.GREY_200),
                    name_field,
                    phone_field,
                    group_field,
                    payment_field,
                    join_date_field
                ], spacing=20),
                padding=ft.padding.all(24)
            )
        )
        self.layout.controls.append(form_card)
        
        # Action buttons
        actions_card = ModernCard(
            content=ft.Container(
                content=ft.Row([
                    self.create_modern_button(
                        "שמור שינויים",
                        ft.Icons.SAVE,
                        ft.Colors.GREEN_600,
                        lambda e: self.save_student(
                            original_name=student['name'],
                            new_data={
                                "id": student.get('id', ''),
                                "name": name_field.value.strip(),
                                "phone": phone_field.value.strip(),
                                "group": group_field.value.strip(),
                                "payment_status": payment_field.value.strip(),
                                "join_date": join_date_field.value.strip(),
                                "payments": student.get('payments', [])
                            }
                        )
                    ),
                    self.create_modern_button(
                        "ביטול",
                        ft.Icons.CANCEL,
                        ft.Colors.GREY_600,
                        lambda e: self.show_students(),
                        variant="outlined"
                    )
                ], spacing=16, alignment=ft.MainAxisAlignment.CENTER),
                padding=ft.padding.all(20)
            )
        )
        self.layout.controls.append(actions_card)
        
        self.page.update()

    def save_student(self, original_name, new_data):
        """Save student with modern feedback"""
        if not all([new_data['name'], new_data['phone'], new_data['group'], new_data['payment_status'], new_data['join_date']]):
            self.show_modern_dialog(
                "שגיאה",
                "יש למלא את כל השדות הנדרשים",
                ft.Icons.ERROR,
                ft.Colors.RED_600
            )
            return

        try:
            with open("data/students.json", encoding="utf-8") as f:
                data = json.load(f)
                students = data.get("students", [])

            for i, student in enumerate(students):
                if student['name'] == original_name:
                    students[i] = new_data
                    break

            with open("data/students.json", 'w', encoding="utf-8") as f:
                json.dump({"students": students}, f, ensure_ascii=False, indent=4)

            self.show_modern_dialog(
                "הצלחה",
                "פרטי התלמידה נשמרו בהצלחה!",
                ft.Icons.CHECK_CIRCLE,
                ft.Colors.GREEN_600,
                callback=lambda: self.show_students()
            )
            
        except Exception as e:
            self.show_modern_dialog(
                "שגיאה",
                f"שגיאה בשמירה: {e}",
                ft.Icons.ERROR,
                ft.Colors.RED_600
            )
            print(f"Error saving: {e}")

    def delete_student(self, student_name):
        """Delete student with modern feedback"""
        try:
            with open("data/students.json", encoding="utf-8") as f:
                data = json.load(f)
                students = data.get("students", [])

            updated_students = [s for s in students if s['name'] != student_name]

            with open("data/students.json", 'w', encoding="utf-8") as f:
                json.dump({"students": updated_students}, f, ensure_ascii=False, indent=4)

            self.show_modern_dialog(
                "הצלחה",
                f"התלמידה {student_name} נמחקה בהצלחה!",
                ft.Icons.CHECK_CIRCLE,
                ft.Colors.GREEN_600,
                callback=lambda: self.show_students()
            )
            
        except Exception as e:
            self.show_modern_dialog(
                "שגיאה",
                f"שגיאה במחיקה: {e}",
                ft.Icons.ERROR,
                ft.Colors.RED_600
            )
            print(f"Error deleting: {e}")

    def show_payments(self, student):
        """Modern payments view"""
        self.clear_layout()
        
        # Header with back button
        header_card = ModernCard(
            content=ft.Container(
                content=ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        icon_color=ft.Colors.GREY_600,
                        on_click=lambda e: self.show_students(),
                        tooltip="חזרה"
                    ),
                    ft.Container(
                        content=ft.Icon(ft.Icons.PAYMENT, size=32, color=ft.Colors.WHITE),
                        bgcolor=ft.Colors.PURPLE_600,
                        border_radius=50,
                        padding=ft.padding.all(12)
                    ),
                    ft.Column([
                        ft.Text(
                            "תשלומים",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREY_800
                        ),
                        ft.Text(
                            f"עבור {student['name']}",
                            size=16,
                            color=ft.Colors.GREY_600
                        )
                    ], spacing=4, expand=True)
                ], spacing=16),
                padding=ft.padding.all(24)
            )
        )
        self.layout.controls.append(header_card)
        
        # Payments list
        payments = student.get('payments', [])
        
        if not payments:
            empty_card = ModernCard(
                content=ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.RECEIPT_LONG_OUTLINED, size=64, color=ft.Colors.GREY_400),
                        ft.Text(
                            "אין תשלומים רשומים",
                            size=20,
                            weight=ft.FontWeight.W_500,
                            color=ft.Colors.GREY_600,
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Text(
                            "הוסיפו את התשלום הראשון",
                            size=14,
                            color=ft.Colors.GREY_500,
                            text_align=ft.TextAlign.CENTER
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12),
                    padding=ft.padding.all(48)
                )
            )
            self.layout.controls.append(empty_card)
        else:
            # Calculate total
            total_paid = sum(
                float(p['amount']) for p in payments
                if p['amount'].replace('.', '', 1).isdigit()
            )
            
            # Summary card
            summary_card = ModernCard(
                content=ft.Container(
                    content=ft.Row([
                        ft.Column([
                            ft.Text("סה״כ תשלומים", size=14, color=ft.Colors.GREY_600),
                            ft.Text(f"{len(payments)}", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_600)
                        ], spacing=4),
                        ft.Container(width=1, height=40, bgcolor=ft.Colors.GREY_300),
                        ft.Column([
                            ft.Text("סה״כ סכום", size=14, color=ft.Colors.GREY_600),
                            ft.Text(f"{total_paid:,.0f}₪", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_600)
                        ], spacing=4)
                    ], spacing=24, alignment=ft.MainAxisAlignment.SPACE_AROUND),
                    padding=ft.padding.all(24)
                ),
                gradient=ft.LinearGradient(
                    colors=[ft.Colors.WHITE, ft.Colors.with_opacity(0.98, ft.Colors.BLUE_50)],
                    begin=ft.alignment.top_left,
                    end=ft.alignment.bottom_right,
                )
            )
            self.layout.controls.append(summary_card)
            
            # Payments list card
            payments_list = ft.Column(spacing=12)
            
            for i, payment in enumerate(payments):
                payment_card = ft.Container(
                    content=ft.Row([
                        ft.Container(
                            content=ft.Icon(ft.Icons.PAYMENT, size=20, color=ft.Colors.WHITE),
                            bgcolor=ft.Colors.GREEN_600,
                            border_radius=25,
                            width=40,
                            height=40,
                            alignment=ft.alignment.center
                        ),
                        ft.Column([
                            ft.Row([
                                ft.Text(
                                    f"{payment['amount']}₪",
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.GREY_800
                                ),
                                ft.Container(
                                    content=ft.Text(
                                        payment['payment_method'],
                                        size=12,
                                        color=ft.Colors.BLUE_600,
                                        weight=ft.FontWeight.W_500
                                    ),
                                    bgcolor=ft.Colors.BLUE_50,
                                    border_radius=12,
                                    padding=ft.padding.symmetric(horizontal=8, vertical=4)
                                )
                            ], spacing=12, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Text(
                                f"📅 {payment['date']}",
                                size=14,
                                color=ft.Colors.GREY_600
                            )
                        ], spacing=4, expand=True)
                    ], spacing=16),
                    bgcolor=ft.Colors.WHITE,
                    border_radius=12,
                    padding=ft.padding.all(16),
                    border=ft.border.all(1, ft.Colors.GREY_200),
                    animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT)
                )
                payments_list.controls.append(payment_card)
            
            payments_card = ModernCard(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "היסטוריית תשלומים",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREY_800
                        ),
                        ft.Divider(height=1, color=ft.Colors.GREY_200),
                        ft.Container(
                            content=payments_list,
                            height=300,
                            padding=ft.padding.symmetric(vertical=8)
                        )
                    ], spacing=16),
                    padding=ft.padding.all(24)
                ),
                hover_effect=False
            )
            self.layout.controls.append(payments_card)
        
        # Action buttons
        actions_card = ModernCard(
            content=ft.Container(
                content=ft.Row([
                    self.create_modern_button(
                        "הוסף תשלום",
                        ft.Icons.ADD_CARD,
                        ft.Colors.PURPLE_600,
                        lambda e: self.show_add_payment_form(student)
                    ),
                    self.create_modern_button(
                        "חזרה לתלמידות",
                        ft.Icons.ARROW_BACK,
                        ft.Colors.GREY_600,
                        lambda e: self.show_students(),
                        variant="outlined"
                    )
                ], spacing=16, alignment=ft.MainAxisAlignment.CENTER),
                padding=ft.padding.all(20)
            )
        )
        self.layout.controls.append(actions_card)
        
        self.page.update()

    def show_add_payment_form(self, student):
        """Modern add payment form"""
        self.clear_layout()
        
        # Header
        header_card = ModernCard(
            content=ft.Container(
                content=ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        icon_color=ft.Colors.GREY_600,
                        on_click=lambda e: self.show_payments(student),
                        tooltip="חזרה"
                    ),
                    ft.Container(
                        content=ft.Icon(ft.Icons.ADD_CARD, size=32, color=ft.Colors.WHITE),
                        bgcolor=ft.Colors.PURPLE_600,
                        border_radius=50,
                        padding=ft.padding.all(12)
                    ),
                    ft.Column([
                        ft.Text(
                            "הוספת תשלום",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREY_800
                        ),
                        ft.Text(
                            f"עבור {student['name']}",
                            size=16,
                            color=ft.Colors.GREY_600
                        )
                    ], spacing=4, expand=True)
                ], spacing=16),
                padding=ft.padding.all(24)
            )
        )
        self.layout.controls.append(header_card)
        
        # Form fields
        self.amount_input = ft.TextField(
            label="סכום התשלום",
            prefix_icon=ft.Icons.ATTACH_MONEY,
            suffix_text="₪",
            border_radius=12,
            bgcolor=ft.Colors.GREY_50,
            border_color=ft.Colors.GREY_300,
            focused_border_color=ft.Colors.PURPLE_600,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=16),
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        self.date_input = ft.TextField(
            label="תאריך התשלום",
            prefix_icon=ft.Icons.CALENDAR_TODAY,
            hint_text="dd/mm/yyyy",
            border_radius=12,
            bgcolor=ft.Colors.GREY_50,
            border_color=ft.Colors.GREY_300,
            focused_border_color=ft.Colors.PURPLE_600,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=16)
        )
        
        # Payment method dropdown
        self.payment_method_dropdown = ft.Dropdown(
            label="אופן תשלום",
            prefix_icon=ft.Icons.PAYMENT,
            border_radius=12,
            bgcolor=ft.Colors.GREY_50,
            border_color=ft.Colors.GREY_300,
            focused_border_color=ft.Colors.PURPLE_600,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=16),
            options=[
                ft.dropdown.Option("מזומן"),
                ft.dropdown.Option("אשראי"),
                ft.dropdown.Option("העברה בנקאית"),
                ft.dropdown.Option("צ'ק"),
                ft.dropdown.Option("ביט"),
                ft.dropdown.Option("פייבוקס")
            ]
        )
        
        # Form card
        form_card = ModernCard(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(
                        "פרטי התשלום",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.GREY_800
                    ),
                    ft.Divider(height=1, color=ft.Colors.GREY_200),
                    self.amount_input,
                    self.date_input,
                    self.payment_method_dropdown,
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.INFO_OUTLINE, size=16, color=ft.Colors.BLUE_600),
                            ft.Text(
                                "התשלום יתווסף להיסטוריית התשלומים של התלמידה",
                                size=12,
                                color=ft.Colors.GREY_600
                            )
                        ], spacing=8),
                        bgcolor=ft.Colors.BLUE_50,
                        border_radius=8,
                        padding=ft.padding.all(12)
                    )
                ], spacing=20),
                padding=ft.padding.all(24)
            )
        )
        self.layout.controls.append(form_card)
        
        # Action buttons
        actions_card = ModernCard(
            content=ft.Container(
                content=ft.Row([
                    self.create_modern_button(
                        "שמור תשלום",
                        ft.Icons.SAVE,
                        ft.Colors.GREEN_600,
                        lambda e: self.save_payment(student, {
                            "amount": self.amount_input.value.strip() if self.amount_input.value else "",
                            "date": self.date_input.value.strip() if self.date_input.value else "",
                            "payment_method": self.payment_method_dropdown.value if self.payment_method_dropdown.value else ""
                        })
                    ),
                    self.create_modern_button(
                        "ביטול",
                        ft.Icons.CANCEL,
                        ft.Colors.GREY_600,
                        lambda e: self.show_payments(student),
                        variant="outlined"
                    )
                ], spacing=16, alignment=ft.MainAxisAlignment.CENTER),
                padding=ft.padding.all(20)
            )
        )
        self.layout.controls.append(actions_card)
        
        self.page.update()

    def save_payment(self, student, payment_data):
        """Save payment with modern validation and feedback"""
        if not all(payment_data.values()):
            self.show_modern_dialog(
                "שגיאה",
                "יש למלא את כל השדות הנדרשים",
                ft.Icons.ERROR,
                ft.Colors.RED_600
            )
            return

        # Validate amount is numeric
        try:
            float(payment_data['amount'])
        except ValueError:
            self.show_modern_dialog(
                "שגיאה",
                "יש להזין סכום תקין (מספר בלבד)",
                ft.Icons.ERROR,
                ft.Colors.RED_600
            )
            return

        try:
            # Load students
            with open("data/students.json", encoding="utf-8") as f:
                data = json.load(f)
                students = data.get("students", [])
            
            # Load groups for pricing
            with open("data/groups.json", encoding="utf-8") as f:
                group_data = json.load(f)
                groups = group_data.get("groups", [])
            
            for s in students:
                if s['name'] == student['name']:
                    s.setdefault("payments", []).append(payment_data)
                    
                    # Calculate total paid
                    total_paid = sum(
                        float(p['amount']) for p in s['payments']
                        if p['amount'].replace('.', '', 1).isdigit()
                    )
                    
                    # Find group price and update payment status
                    group_name = s.get("group")
                    group = next((g for g in groups if g['name'] == group_name), None)
                    
                    if group:
                        group_price = float(group.get("price", "0"))
                        if total_paid >= group_price:
                            s['payment_status'] = "שולם"
                        else:
                            s['payment_status'] = f"חוב: {group_price - total_paid:,.0f}₪"
                    else:
                        s['payment_status'] = "לא נמצא מחיר קבוצה"
                    break
            
            # Save file
            with open("data/students.json", 'w', encoding="utf-8") as f:
                json.dump({"students": students}, f, ensure_ascii=False, indent=4)
            
            self.show_modern_dialog(
                "הצלחה",
                "התשלום נשמר בהצלחה!",
                ft.Icons.CHECK_CIRCLE,
                ft.Colors.GREEN_600,
                callback=lambda: self.show_payments(student)
            )
            
        except Exception as e:
            self.show_modern_dialog(
                "שגיאה",
                f"שגיאה בשמירת תשלום: {e}",
                ft.Icons.ERROR,
                ft.Colors.RED_600
            )
            print(f"Error saving payment: {e}")

    def show_modern_dialog(self, title, message, icon, color, callback=None):
        """Show modern styled dialog"""
        def close_dialog(e):
            dialog.open = False
            self.page.update()
            if callback:
                callback()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(icon, color=color, size=24),
                ft.Text(title, size=20, weight=ft.FontWeight.BOLD)
            ], spacing=12),
            content=ft.Container(
                content=ft.Text(
                    message,
                    size=16,
                    color=ft.Colors.GREY_700
                ),
                padding=ft.padding.symmetric(vertical=16)
            ),
            actions=[
                ft.ElevatedButton(
                    "אישור",
                    on_click=close_dialog,
                    bgcolor=color,
                    color=ft.Colors.WHITE,
                    style=ft.ButtonStyle(
                        padding=ft.padding.symmetric(horizontal=24, vertical=12),
                        shape=ft.RoundedRectangleBorder(radius=8)
                    )
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            shape=ft.RoundedRectangleBorder(radius=16)
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

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

    def close_dialog(self):
        """Close any open dialog"""
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()

    def close_dialog_and_refresh(self):
        """Close dialog and refresh students view"""
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()
        self.show_students()

    def close_dialog_and_show_payments(self, student):
        """Close dialog and show payments view"""
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()
        self.show_payments(student)
