import flet as ft
from components.add_groups_form_fields import FormFields
from utils.groups_data_manager import GroupsDataManager


class AddGroupPage:
    def __init__(self, page, navigation_callback, groups_page):
        self.page = page
        self.navigation_callback = navigation_callback
        self.groups_page = groups_page
        self.data_manager = GroupsDataManager()
        
        self.form_fields = FormFields.create_group_form_fields()
        
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
                ft.Container(height=10),
                
                ft.Row([
                    ft.Container(content=self.form_fields['name'], expand=1),
                    ft.Container(width=20),
                    ft.Container(content=self.form_fields['location'], expand=1),
                ]),
                
                ft.Row([
                    ft.Container(content=self.form_fields['price'], expand=1),
                    ft.Container(width=20),
                    ft.Container(content=self.form_fields['age'], expand=1),
                ]),
                
                self.form_fields['teacher'],
                
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
                ft.Container(width=15),
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
        """Save group with validation"""
        group_data = {
            "name": self.form_fields['name'].value.strip() if self.form_fields['name'].value else "",
            "location": self.form_fields['location'].value.strip() if self.form_fields['location'].value else "",
            "price": self.form_fields['price'].value.strip() if self.form_fields['price'].value else "",
            "age_group": self.form_fields['age'].value.strip() if self.form_fields['age'].value else "",
            "teacher": self.form_fields['teacher'].value.strip() if self.form_fields['teacher'].value else "",
        }
        
        is_valid, error_message = self.data_manager.validate_group_data(group_data)
        if not is_valid:
            self.show_snackbar(error_message, "#f56565")
            return
        
        success, message = self.data_manager.save_group(group_data)
        
        if success:
            self.show_snackbar(f'הקבוצה "{group_data["name"]}" נוספה בהצלחה!', "#48bb78")
            self.clear_form()

            if self.groups_page:
                self.groups_page.refresh()
            self.navigation_callback(None, 1)
        else:
            self.show_snackbar(message, "#f56565")

    def show_snackbar(self, message, color):
        """Show snackbar message"""
        icon = ft.Icons.CHECK_CIRCLE if color == "#48bb78" else ft.Icons.ERROR
        
        self.page.snack_bar = ft.SnackBar(
            content=ft.Row([
                ft.Icon(icon, color="white", size=20),
                ft.Text(message, color="white", size=14, weight=ft.FontWeight.W_500)
            ], spacing=10),
            bgcolor=color,
            duration=3000,
        )
        self.page.snack_bar.open = True
        self.page.update()

    def clear_form(self):
        """Clear all form fields"""
        for field in self.form_fields.values():
            field.value = ""

    def go_back(self, e):
        """Navigate back to groups page"""
        if self.groups_page:
            self.groups_page.refresh()
        self.navigation_callback(None, 1)
