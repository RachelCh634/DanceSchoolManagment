import json
import flet as ft
from datetime import datetime


class ModernCard(ft.Container):
    def __init__(self, content=None, hover_effect=True, gradient=None, **kwargs):
        super().__init__(
            content=content,
            bgcolor=ft.Colors.WHITE if not gradient else None,
            gradient=gradient,
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


class AddStudentPage:
    def __init__(self, page, navigation_callback, group_name):
        self.page = page
        self.navigation_callback = navigation_callback
        self.group_name = group_name
        
        # Main layout
        self.layout = ft.Column(
            spacing=24,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            animate_opacity=300,
        )
        
        # Form fields
        self.name_input = None
        self.phone_input = None
        self.id_input = None
        self.group_dropdown = None
        self.payment_status_dropdown = None
        self.join_date_input = None
        
        self.show_add_student_form()

    def get_view(self):
        return ft.Container(
            content=self.layout,
            bgcolor=ft.Colors.WHITE,
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

    def show_add_student_form(self):
        self.clear_layout()
        
        # Modern Header
        header_card = ModernCard(
            content=ft.Container(
                content=ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        icon_color=ft.Colors.GREY_600,
                        on_click=self.go_back,
                        tooltip="חזרה"
                    ),
                    ft.Container(
                        content=ft.Icon(ft.Icons.PERSON_ADD, size=32, color=ft.Colors.WHITE),
                        bgcolor=ft.Colors.GREEN_600,
                        border_radius=50,
                        padding=ft.padding.all(12)
                    ),
                    ft.Column([
                        ft.Text(
                            "הוספת תלמידה חדשה",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREY_800
                        ),
                        ft.Text(
                            f"לקבוצת {self.group_name}",
                            size=16,
                            color=ft.Colors.GREY_600
                        )
                    ], spacing=4, expand=True)
                ], spacing=16),
                padding=ft.padding.all(24)
            ),
            gradient=ft.LinearGradient(
                colors=[ft.Colors.WHITE, ft.Colors.with_opacity(0.98, ft.Colors.GREEN_50)],
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
            )
        )
        self.layout.controls.append(header_card)
        
        # Form Card
        self.create_form_fields()
        
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
                    
                    # Personal Info Section
                    ft.Container(
                        content=ft.Column([
                            ft.Text(
                                "👤 פרטים אישיים",
                                size=16,
                                weight=ft.FontWeight.W_500,
                                color=ft.Colors.GREY_700
                            ),
                            self.name_input,
                            self.id_input,
                            self.phone_input,
                        ], spacing=16),
                        bgcolor=ft.Colors.GREY_50,
                        border_radius=12,
                        padding=ft.padding.all(16)
                    ),
                    
                    # Group & Payment Section
                    ft.Container(
                        content=ft.Column([
                            ft.Text(
                                "🏫 פרטי קבוצה ותשלום",
                                size=16,
                                weight=ft.FontWeight.W_500,
                                color=ft.Colors.GREY_700
                            ),
                            self.group_dropdown,
                            self.payment_status_dropdown,
                            self.join_date_input,
                        ], spacing=16),
                        bgcolor=ft.Colors.BLUE_50,
                        border_radius=12,
                        padding=ft.padding.all(16)
                    ),
                    
                    # Info box
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.INFO_OUTLINE, size=16, color=ft.Colors.BLUE_600),
                            ft.Text(
                                "כל השדות נדרשים למילוי. התלמידה תתווסף לקבוצה שנבחרה.",
                                size=12,
                                color=ft.Colors.GREY_600
                            )
                        ], spacing=8),
                        bgcolor=ft.Colors.BLUE_50,
                        border_radius=8,
                        padding=ft.padding.all(12)
                    )
                ], spacing=24),
                padding=ft.padding.all(24)
            )
        )
        self.layout.controls.append(form_card)
        
        # Action Buttons
        actions_card = ModernCard(
            content=ft.Container(
                content=ft.Row([
                    self.create_modern_button(
                        "הוסף תלמידה",
                        ft.Icons.SAVE,
                        ft.Colors.GREEN_600,
                        self.add_student
                    ),
                    self.create_modern_button(
                        "ביטול",
                        ft.Icons.CANCEL,
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

    def create_form_fields(self):
        """Create all form input fields"""
        
        # Name input
        self.name_input = ft.TextField(
            label="שם התלמידה",
            hint_text="הכנסי שם מלא",
            prefix_icon=ft.Icons.PERSON,
            border_radius=12,
            bgcolor=ft.Colors.WHITE,
            border_color=ft.Colors.GREY_300,
            focused_border_color=ft.Colors.GREEN_600,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=16),
            text_align=ft.TextAlign.RIGHT
        )
        
        # ID input
        self.id_input = ft.TextField(
            label="תעודת זהות",
            hint_text="הכנסי מספר תעודת זהות",
            prefix_icon=ft.Icons.BADGE,
            border_radius=12,
            bgcolor=ft.Colors.WHITE,
            border_color=ft.Colors.GREY_300,
            focused_border_color=ft.Colors.GREEN_600,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=16),
            keyboard_type=ft.KeyboardType.NUMBER,
            text_align=ft.TextAlign.RIGHT
        )
        
        # Phone input
        self.phone_input = ft.TextField(
            label="מספר טלפון",
            hint_text="הכנסי מספר טלפון",
            prefix_icon=ft.Icons.PHONE,
            border_radius=12,
            bgcolor=ft.Colors.WHITE,
            border_color=ft.Colors.GREY_300,
            focused_border_color=ft.Colors.GREEN_600,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=16),
            keyboard_type=ft.KeyboardType.PHONE,
            text_align=ft.TextAlign.RIGHT
        )
        
        # Group dropdown
        self.group_dropdown = ft.Dropdown(
            label="קבוצה",
            prefix_icon=ft.Icons.GROUP,
            border_radius=12,
            bgcolor=ft.Colors.WHITE,
            border_color=ft.Colors.GREY_300,
            focused_border_color=ft.Colors.GREEN_600,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=16),
            options=[]
        )
        self.load_groups()
        
        # Payment status dropdown
        self.payment_status_dropdown = ft.Dropdown(
            label="סטטוס תשלום",
            prefix_icon=ft.Icons.PAYMENT,
            border_radius=12,
            bgcolor=ft.Colors.WHITE,
            border_color=ft.Colors.GREY_300,
            focused_border_color=ft.Colors.GREEN_600,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=16),
            options=[
                ft.dropdown.Option("חוב"),
                ft.dropdown.Option("יתרת זכות"),
                ft.dropdown.Option("שולם")
            ],
            value="חוב"  # Default value
        )
        
        # Join date input
        current_date = datetime.now().strftime("%d/%m/%Y")
        self.join_date_input = ft.TextField(
            label="תאריך הצטרפות",
            hint_text="dd/mm/yyyy",
            prefix_icon=ft.Icons.CALENDAR_TODAY,
            border_radius=12,
            bgcolor=ft.Colors.WHITE,
            border_color=ft.Colors.GREY_300,
            focused_border_color=ft.Colors.GREEN_600,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=16),
            value=current_date,
            text_align=ft.TextAlign.RIGHT
        )

    def load_groups(self):
        """Load groups from JSON file"""
        try:
            with open("data/groups.json", encoding="utf-8") as f:
                data = json.load(f)
                groups = data.get("groups", [])
                
                # Clear existing options
                self.group_dropdown.options.clear()
                
                # Add groups to dropdown
                for group in groups:
                    self.group_dropdown.options.append(
                        ft.dropdown.Option(group["name"])
                    )
                
                # Set current group as selected
                if self.group_name:
                    self.group_dropdown.value = self.group_name
                    
        except Exception as e:
            print(f"Error loading groups: {e}")
            self.show_modern_dialog(
                "שגיאה",
                "שגיאה בטעינת רשימת הקבוצות",
                ft.Icons.ERROR,
                ft.Colors.RED_600
            )

    def add_student(self, e=None):
        """Add new student with validation"""
        
        # Get form values
        student_id = self.id_input.value.strip() if self.id_input.value else ""
        name = self.name_input.value.strip() if self.name_input.value else ""
        phone = self.phone_input.value.strip() if self.phone_input.value else ""
        group = self.group_dropdown.value if self.group_dropdown.value else ""
        payment_status = self.payment_status_dropdown.value if self.payment_status_dropdown.value else ""
        join_date = self.join_date_input.value.strip() if self.join_date_input.value else ""
        
        # Validation
        if not all([student_id, name, phone, group, payment_status, join_date]):
            self.show_modern_dialog(
                "שגיאה",
                "יש למלא את כל השדות הנדרשים",
                ft.Icons.ERROR,
                ft.Colors.RED_600
            )
            return
        
        # Validate ID format (basic validation)
        if not student_id.isdigit() or len(student_id) != 9:
            self.show_modern_dialog(
                "שגיאה",
                "מספר תעודת זהות חייב להכיל 9 ספרות בלבד",
                ft.Icons.ERROR,
                ft.Colors.RED_600
            )
            return
        
        try:
            # Load existing students
            try:
                with open("data/students.json", encoding="utf-8") as f:
                    students_data = json.load(f)
            except FileNotFoundError:
                students_data = {"students": []}
            if "students" not in students_data or not isinstance(students_data["students"], list):
                students_data["students"] = []

            # Check if student with same ID already exists
            for student in students_data["students"]:
                if student.get("id") == student_id:
                    self.show_modern_dialog(
                        "שגיאה",
                        f"תלמידה עם ת.ז. {student_id} כבר קיימת במערכת",
                        ft.Icons.ERROR,
                        ft.Colors.RED_600
                    )
                    return

            # Create new student object
            new_student = {
                "id": student_id,
                "name": name,
                "phone": phone,
                "group": group,
                "payment_status": payment_status,
                "join_date": join_date,
                "payments": []  # Initialize empty payments array
            }

            # Add to students list
            students_data["students"].append(new_student)

            # Save to file
            with open("data/students.json", 'w', encoding="utf-8") as f:
                json.dump(students_data, f, ensure_ascii=False, indent=4)

            # Show success message
            self.go_back()
            
        except Exception as e:
            print(f"Error saving student: {e}")
            self.show_modern_dialog(
                "שגיאה",
                f"שגיאה בשמירת התלמידה: {str(e)}",
                ft.Icons.ERROR,
                ft.Colors.RED_600
            )

    def show_modern_dialog(self, title, message, icon, color):
        """Show a modern styled dialog"""
        def close_dialog(e):
            dialog.open = False
            self.page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(icon, color=color, size=24),
                ft.Text(title, size=18, weight=ft.FontWeight.BOLD, color=color)
            ], spacing=12),
            content=ft.Container(
                content=ft.Text(
                    message,
                    size=14,
                    color=ft.Colors.GREY_700,
                    text_align=ft.TextAlign.RIGHT
                ),
                padding=ft.padding.symmetric(vertical=16)
            ),
            actions=[
                ft.TextButton(
                    content=ft.Text("אישור", size=14, weight=ft.FontWeight.W_500),
                    style=ft.ButtonStyle(
                        color=color,
                        bgcolor={
                            "": ft.Colors.TRANSPARENT,
                            "hovered": ft.Colors.with_opacity(0.1, color)
                        }
                    ),
                    on_click=close_dialog
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            shape=ft.RoundedRectangleBorder(radius=16),
            bgcolor=ft.Colors.WHITE,
            title_padding=ft.padding.all(24),
            content_padding=ft.padding.symmetric(horizontal=24),
            actions_padding=ft.padding.all(24)
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def show_success_dialog(self):
        """Show success dialog and navigate back"""
        def close_and_navigate(e):
            dialog.open = False
            self.page.update()
            self.go_back()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN_600, size=24),
                ft.Text("הצלחה!", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_600)
            ], spacing=12),
            content=ft.Container(
                content=ft.Column([
                    ft.Text(
                        "התלמידה נוספה בהצלחה למערכת!",
                        size=14,
                        color=ft.Colors.GREY_700,
                        text_align=ft.TextAlign.RIGHT
                    ),
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.INFO_OUTLINE, size=16, color=ft.Colors.BLUE_600),
                            ft.Text(
                                "תועברי חזרה לרשימת התלמידות",
                                size=12,
                                color=ft.Colors.GREY_600
                            )
                        ], spacing=8),
                        bgcolor=ft.Colors.BLUE_50,
                        border_radius=8,
                        padding=ft.padding.all(12),
                        margin=ft.margin.only(top=12)
                    )
                ], spacing=8),
                padding=ft.padding.symmetric(vertical=16)
            ),
            actions=[
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Icon(ft.Icons.ARROW_BACK, size=16, color=ft.Colors.WHITE),
                        ft.Text("חזרה לרשימה", size=14, weight=ft.FontWeight.W_500, color=ft.Colors.WHITE)
                    ], spacing=8, tight=True),
                    bgcolor=ft.Colors.GREEN_600,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        padding=ft.padding.symmetric(horizontal=16, vertical=8)
                    ),
                    on_click=close_and_navigate
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            shape=ft.RoundedRectangleBorder(radius=16),
            bgcolor=ft.Colors.WHITE,
            title_padding=ft.padding.all(24),
            content_padding=ft.padding.symmetric(horizontal=24),
            actions_padding=ft.padding.all(24)
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def go_back(self, e=None):
        """Navigate back to students page"""
        # Import here to avoid circular imports
        from students_page import StudentsPage
        students_page = StudentsPage(self.page, self.navigation_callback, self.group_name)
        self.navigation_callback(students_page)

    def clear_layout(self):
        """Clear the layout"""
        self.layout.controls.clear()
