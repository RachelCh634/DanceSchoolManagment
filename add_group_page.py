import json
import flet as ft

class AddGroupPage:
    def __init__(self, page, navigation_callback, groups_page):
        self.page = page
        self.navigation_callback = navigation_callback
        self.groups_page = groups_page
        
        # Form fields
        self.group_name_input = ft.TextField(
            label="שם הקבוצה",
            hint_text="הכנס את שם הקבוצה",
            border_radius=8,
            bgcolor="#f7fafc",
            border_color="#e2e8f0",
            focused_border_color="#4299e1",
            text_size=14,
            label_style=ft.TextStyle(color="#4a5568"),
        )
        
        self.group_location_input = ft.TextField(
            label="מיקום הקבוצה",
            hint_text="הכנס את מיקום הקבוצה",
            border_radius=8,
            bgcolor="#f7fafc",
            border_color="#e2e8f0",
            focused_border_color="#4299e1",
            text_size=14,
            label_style=ft.TextStyle(color="#4a5568"),
        )
        
        self.group_price_input = ft.TextField(
            label="עלות הקבוצה",
            hint_text="הכנס את עלות הקבוצה",
            border_radius=8,
            bgcolor="#f7fafc",
            border_color="#e2e8f0",
            focused_border_color="#4299e1",
            text_size=14,
            label_style=ft.TextStyle(color="#4a5568"),
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        
        self.group_age_input = ft.TextField(
            label="קבוצת גילאים",
            hint_text="לדוגמה: 6-8 שנים",
            border_radius=8,
            bgcolor="#f7fafc",
            border_color="#e2e8f0",
            focused_border_color="#4299e1",
            text_size=14,
            label_style=ft.TextStyle(color="#4a5568"),
        )
        
        self.group_teacher_input = ft.TextField(
            label="שם המורה",
            hint_text="הכנס את שם המורה",
            border_radius=8,
            bgcolor="#f7fafc",
            border_color="#e2e8f0",
            focused_border_color="#4299e1",
            text_size=14,
            label_style=ft.TextStyle(color="#4a5568"),
        )
        
        # Main layout
        self.main_layout = ft.Column(
            controls=[
                self.create_header(),
                self.create_form_section(),
                self.create_footer()
            ],
            expand=True,
            spacing=0
        )

    def create_header(self):
        """Create clean header section"""
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Column([
                        ft.Text(
                            "הוספת קבוצה חדשה",
                            size=28,
                            weight=ft.FontWeight.BOLD,
                            color="#1a202c"
                        ),
                        ft.Text(
                            "מלא את הפרטים ליצירת קבוצה חדשה במערכת",
                            size=16,
                            color="#718096"
                        ),
                    ], spacing=4, expand=True),
                ], alignment=ft.MainAxisAlignment.START),
                ft.Divider(color="#e2e8f0", height=1),
            ], spacing=20),
            padding=ft.padding.all(30),
            bgcolor="white"
        )

    def create_form_section(self):
        """Create the form section"""
        form_card = ft.Container(
            content=ft.Column([
                ft.Text(
                    "פרטי הקבוצה",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color="#1a202c"
                ),
                ft.Container(height=10),  # Spacer
                
                # Form fields in a grid layout
                ft.Row([
                    ft.Container(content=self.group_name_input, expand=1),
                    ft.Container(width=20),  # Spacer
                    ft.Container(content=self.group_location_input, expand=1),
                ]),
                
                ft.Row([
                    ft.Container(content=self.group_price_input, expand=1),
                    ft.Container(width=20),  # Spacer
                    ft.Container(content=self.group_age_input, expand=1),
                ]),
                
                self.group_teacher_input,
                
            ], spacing=20),
            bgcolor="white",
            border_radius=12,
            padding=ft.padding.all(30),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.06, ft.Colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
        )
        
        return ft.Container(
            content=form_card,
            padding=ft.padding.symmetric(horizontal=30),
            expand=True
        )

    def create_footer(self):
        """Create footer with action buttons"""
        return ft.Container(
            content=ft.Row([
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Icon(ft.Icons.ARROW_BACK, size=18, color="#718096"),
                        ft.Text("ביטול", color="#718096", size=14, weight=ft.FontWeight.W_500)
                    ], spacing=8, tight=True),
                    bgcolor="white",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        padding=ft.padding.symmetric(horizontal=20, vertical=12),
                        elevation=0,
                        side=ft.BorderSide(width=1, color="#e2e8f0")
                    ),
                    on_click=self.go_back
                ),
                ft.Container(width=15),  # Spacer
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Icon(ft.Icons.SAVE, size=18, color="white"),
                        ft.Text("שמור קבוצה", color="white", size=14, weight=ft.FontWeight.W_500)
                    ], spacing=8, tight=True),
                    bgcolor="#48bb78",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        padding=ft.padding.symmetric(horizontal=20, vertical=12),
                        elevation=0,
                    ),
                    on_click=self.save_group
                )
            ], alignment=ft.MainAxisAlignment.CENTER),
            padding=ft.padding.all(30),
            bgcolor="white"
        )

    def get_view(self):
        return self.main_layout

    def save_group(self, e):
        name = self.group_name_input.value.strip() if self.group_name_input.value else ""
        location = self.group_location_input.value.strip() if self.group_location_input.value else ""
        price = self.group_price_input.value.strip() if self.group_price_input.value else ""
        age_group = self.group_age_input.value.strip() if self.group_age_input.value else ""
        teacher = self.group_teacher_input.value.strip() if self.group_teacher_input.value else ""

        # Validation
        if not name or not location or not price or not age_group or not teacher:
            # Show error snackbar
            self.page.snack_bar = ft.SnackBar(
                content=ft.Row([
                    ft.Icon(ft.Icons.ERROR, color="white", size=20),
                    ft.Text("נא למלא את כל השדות", color="white", size=14, weight=ft.FontWeight.W_500)
                ], spacing=10),
                bgcolor="#f56565",
                duration=3000,
            )
            self.page.snack_bar.open = True
            self.page.update()
            return

        # Load existing data
        try:
            with open("data/groups.json", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {"groups": []}

        # Create new group
        existing_ids = [group.get("id", 0) for group in data.get("groups", [])]
        new_id = max(existing_ids) + 1 if existing_ids else 1

        new_group = {
            "id": new_id,
            "name": name,
            "location": location,
            "price": price,
            "age_group": age_group,
            "teacher": teacher,
            "students": []
        }

        data["groups"].append(new_group)

        # Save to file
        try:
            with open("data/groups.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            # Show success snackbar
            self.page.snack_bar = ft.SnackBar(
                content=ft.Row([
                    ft.Icon(ft.Icons.CHECK_CIRCLE, color="white", size=24),
                    ft.Text(f'הקבוצה "{name}" נוספה בהצלחה!', 
                           color="white", size=16, weight=ft.FontWeight.W_500)
                ], spacing=12),
                bgcolor="#48bb78",
                duration=2000,
            )
            self.page.snack_bar.open = True
            self.page.update()

            # Clear form and go back
            self.group_name_input.value = ""
            self.group_location_input.value = ""
            self.group_price_input.value = ""
            self.group_age_input.value = ""
            self.group_teacher_input.value = ""
            
            # Refresh groups page and navigate back
            if self.groups_page:
                self.groups_page.refresh()
            self.navigation_callback(None, 1)

        except Exception as ex:
            # Show error snackbar
            self.page.snack_bar = ft.SnackBar(
                content=ft.Row([
                    ft.Icon(ft.Icons.ERROR, color="white", size=20),
                    ft.Text(f"שגיאה בשמירת הקובץ: {ex}", color="white", size=14, weight=ft.FontWeight.W_500)
                ], spacing=10),
                bgcolor="#f56565",
                duration=4000,
            )
            self.page.snack_bar.open = True
            self.page.update()

    def go_back(self, e):
        """Navigate back to groups page"""
        if self.groups_page:
            self.groups_page.refresh()
        self.navigation_callback(None, 1)
