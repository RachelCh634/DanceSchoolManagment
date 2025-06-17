import flet as ft
from components.add_groups_form_fields import FormFields
from utils.groups_data_manager import GroupsDataManager


class AddGroupPage:
    def __init__(self, page, navigation_callback, groups_page):
        self.page = page
        self.navigation_callback = navigation_callback
        self.groups_page = groups_page
        self.data_manager = GroupsDataManager()

        self.form_state = {
            'name': '',
            'location': '',
            'price': '',
            'age': '',
            'teacher': '',
            'start_date': '',
            'day_of_week': '',
            'phone':'',
            'email':'',
        }

        self.form_fields = self._create_form_fields()
        self.main_layout = self._render()

    def _create_form_fields(self):
        """Create styled form fields with modern React-like approach"""
        return {
            'name': self._create_text_field(
                label="שם הקבוצה",
                hint="הכנס שם קבוצה",
                icon=ft.Icons.BADGE_OUTLINED,
                key='name'
            ),
            'location': self._create_text_field(
                label="מיקום",
                hint="מיקום הקבוצה",
                icon=ft.Icons.LOCATION_ON_OUTLINED,
                key='location'
            ),
            'price': self._create_text_field(
                label="מחיר",
                hint="מחיר לשיעור",
                icon=ft.Icons.PAYMENTS_OUTLINED,
                suffix="₪",
                keyboard_type=ft.KeyboardType.NUMBER,
                key='price'
            ),
            'age': self._create_text_field(
                label="קבוצת גיל",
                hint="טווח גילאים",
                icon=ft.Icons.GROUPS_OUTLINED,
                key='age'
            ),
            'teacher': self._create_text_field(
                label="מורה/מדריך",
                hint="שם המורה או המדריך",
                icon=ft.Icons.PERSON_OUTLINE,
                key='teacher'
            ),
            'start_date': self._create_text_field(
                label="תאריך התחלה",
                hint="dd/mm/yyyy",
                icon=ft.Icons.DATE_RANGE_OUTLINED,
                key='start_date'
            ),
            'day_of_week': self._create_text_field(
                label="יום בשבוע",
                hint="לדוג' ראשון, שני, שלישי...",
                icon=ft.Icons.CALENDAR_VIEW_WEEK,
                key='day_of_week'
            ),
            'phone': self._create_text_field(
                label="טלפון",
                hint="מספר טלפון",
                icon=ft.Icons.PHONE,
                keyboard_type=ft.KeyboardType.PHONE,
                key='phone'
            ),
            'email': self._create_text_field(
                label="אימייל",
                hint="כתובת אימייל",
                icon=ft.Icons.EMAIL_OUTLINED,
                keyboard_type=ft.KeyboardType.EMAIL,
                key='email'
            ),

        }

    def _create_text_field(self, label, hint, icon, key, suffix=None, keyboard_type=None):
        """Create a modern text field component (React-like component)"""
        field = ft.TextField(
            label=label,
            hint_text=hint,
            prefix_icon=icon,
            suffix_text=suffix,
            keyboard_type=keyboard_type,
            border_radius=12,
            bgcolor="#fafbfc",
            border_color="#e1e7ef",
            focused_border_color="#3b82f6",
            focused_bgcolor="#ffffff",
            label_style=ft.TextStyle(
                color="#64748b", 
                size=14,
                weight=ft.FontWeight.W_500
            ),
            text_style=ft.TextStyle(
                color="#0f172a", 
                size=16,
                weight=ft.FontWeight.W_400
            ),
            hint_style=ft.TextStyle(
                color="#94a3b8",
                size=14
            ),
            content_padding=ft.padding.symmetric(horizontal=16, vertical=14),
            cursor_color="#3b82f6",
            selection_color=ft.Colors.with_opacity(0.2, "#3b82f6"),
            on_change=lambda e, field_key=key: self._handle_field_change(field_key, e.control.value)
        )
        return field

    def _handle_field_change(self, key, value):
        """Handle field changes (React-like state management)"""
        self.form_state[key] = value

    def _render(self):
        """Main render method (React-like)"""
        return ft.Column(
            controls=[
                self._render_header(),
                self._render_form_section(),
                self._render_footer()
            ],
            expand=True,
            spacing=0,
            scroll=ft.ScrollMode.AUTO
        )

    def _render_header(self):
        """Render header component"""
        return ft.Container(
            content=ft.Column([
                # Title Section
                ft.Row([
                    ft.Container(
                        content=ft.Icon(
                            ft.Icons.ADD_CIRCLE_OUTLINE,
                            size=36,
                            color="#3b82f6"
                        ),
                        bgcolor=ft.Colors.with_opacity(0.1, "#3b82f6"),
                        border_radius=12,
                        padding=ft.padding.all(12)
                    ),
                    ft.Container(width=16),
                    ft.Column([
                        ft.Text(
                            "הוספת קבוצה חדשה",
                            size=28,
                            weight=ft.FontWeight.BOLD,
                            color="#0f172a"
                        ),
                        ft.Text(
                            "מלא את הפרטים הנדרשים ליצירת קבוצה חדשה במערכת",
                            size=16,
                            color="#64748b",
                            weight=ft.FontWeight.W_400
                        ),
                    ], spacing=4, expand=True),
                ], alignment=ft.MainAxisAlignment.START),
                
                ft.Container(height=24),
                ft.Divider(color="#e2e8f0", height=1, thickness=1),
            ], spacing=16),
            padding=ft.padding.all(32),
            bgcolor="#ffffff",
            border=ft.border.only(bottom=ft.BorderSide(1, "#f1f5f9"))
        )

    def _render_form_section(self):
        """Render form section component"""
        return ft.Container(
            content=self._render_form_card(),
            padding=ft.padding.symmetric(horizontal=32, vertical=24),
            expand=True,
            bgcolor="#f8fafc"
        )

    def _render_form_card(self):
        """Render the main form card"""
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    self._render_section_header(),
                    
                    ft.Container(height=28),
                    
                    self._render_form_grid(),
                    
                ], spacing=0),
                padding=ft.padding.all(32)
            ),
            elevation=1,
            shadow_color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK),
            surface_tint_color="#ffffff",
            margin=ft.margin.all(0)
        )

    def _render_section_header(self):
        """Render section header"""
        return ft.Row([
            ft.Container(
                content=ft.Icon(ft.Icons.EDIT_OUTLINED, color="#3b82f6", size=20),
                bgcolor=ft.Colors.with_opacity(0.1, "#3b82f6"),
                border_radius=8,
                padding=ft.padding.all(8)
            ),
            ft.Container(width=12),
            ft.Text(
                "פרטי הקבוצה",
                size=20,
                weight=ft.FontWeight.BOLD,
                color="#0f172a"
            ),
        ])

    def _render_form_grid(self):
        """Render form fields in a responsive grid"""
        return ft.Column([
            ft.ResponsiveRow([
                ft.Container(
                    content=self.form_fields['name'],
                    col={"xs": 12, "sm": 12, "md": 6},
                    padding=ft.padding.only(bottom=20, right=12)
                ),
                ft.Container(
                    content=self.form_fields['location'],
                    col={"xs": 12, "sm": 12, "md": 6},
                    padding=ft.padding.only(bottom=20, left=12)
                ),
            ]),

            ft.ResponsiveRow([
                ft.Container(
                    content=self.form_fields['price'],
                    col={"xs": 12, "sm": 12, "md": 6},
                    padding=ft.padding.only(bottom=20, right=12)
                ),
                ft.Container(
                    content=self.form_fields['age'],
                    col={"xs": 12, "sm": 12, "md": 6},
                    padding=ft.padding.only(bottom=20, left=12)
                ),
            ]),

            ft.ResponsiveRow([
                ft.Container(
                    content=self.form_fields['start_date'],
                    col={"xs": 12, "sm": 12, "md": 6},
                    padding=ft.padding.only(bottom=20, right=12)
                ),
                ft.Container(
                    content=self.form_fields['day_of_week'],
                    col={"xs": 12, "sm": 12, "md": 6},
                    padding=ft.padding.only(bottom=20, left=12)
                ),
            ]),

            ft.ResponsiveRow([
                ft.Container(
                    content=self.form_fields['teacher'],
                    col={"xs": 12, "sm": 12, "md": 12},
                    padding=ft.padding.only(bottom=20, right=12)
                ),
            ]),


            ft.ResponsiveRow([
                ft.Container(
                    content=self.form_fields['phone'],
                    col={"xs": 12, "sm": 12, "md":6},
                    padding=ft.padding.only(bottom=20, right=12)
                ),
                ft.Container(
                    content=self.form_fields['email'],
                    col={"xs": 12, "sm": 12, "md": 6},
                    padding=ft.padding.only(bottom=20, left=12)
                ),
            ]),
        ], spacing=0)

    def _render_footer(self):
        """Render footer with modern action buttons"""
        return ft.Container(
            content=ft.Column([
                ft.Divider(color="#e2e8f0", height=1),
                ft.Container(height=16),
                ft.Row([
                    self._render_cancel_button(),
                    ft.Container(width=20),
                    self._render_save_button(),
                ], 
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=0
                ),
            ], spacing=0),
            padding=ft.padding.symmetric(horizontal=32, vertical=24),
            bgcolor="#fafbfc",
        )

    def _render_cancel_button(self):
        """Render elegant cancel button component"""
        return ft.Container(
            content=ft.TextButton(
                content=ft.Row([
                    ft.Icon(ft.Icons.ARROW_BACK_ROUNDED, size=18, color="#64748b"),
                    ft.Text("ביטול", color="#64748b", size=15, weight=ft.FontWeight.W_600)
                ], spacing=10, tight=True),
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=14),
                    padding=ft.padding.symmetric(horizontal=28, vertical=16),
                    bgcolor={
                        ft.ControlState.DEFAULT: "#ffffff",
                        ft.ControlState.HOVERED: "#f8fafc",
                        ft.ControlState.PRESSED: "#f1f5f9",
                    },
                    overlay_color="transparent",
                    side={
                        ft.ControlState.DEFAULT: ft.BorderSide(1, "#e2e8f0"),
                        ft.ControlState.HOVERED: ft.BorderSide(1, "#cbd5e1"),
                    }
                ),
                on_click=self._handle_cancel
            ),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.04, ft.Colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
        )

    def _render_save_button(self):
        """Render beautiful save button component"""
        return ft.Container(
            content=ft.ElevatedButton(
                content=ft.Row([
                    ft.Icon(ft.Icons.BOOKMARK_ADD_OUTLINED, size=20, color="white"),
                    ft.Text("שמור קבוצה", color="white", size=15, weight=ft.FontWeight.BOLD)
                ], spacing=12, tight=True),
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=14),
                    padding=ft.padding.symmetric(horizontal=32, vertical=18),
                    elevation={
                        ft.ControlState.DEFAULT: 3,
                        ft.ControlState.HOVERED: 6,
                        ft.ControlState.PRESSED: 1,
                    },
                    shadow_color=ft.Colors.with_opacity(0.3, "#059669"),
                    bgcolor={
                        ft.ControlState.DEFAULT: "#10b981",
                        ft.ControlState.HOVERED: "#059669",
                        ft.ControlState.PRESSED: "#047857",
                    },
                    overlay_color={
                        ft.ControlState.HOVERED: ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                        ft.ControlState.PRESSED: ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
                    }
                ),
                on_click=self._handle_save
            ),
            animate_scale=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
        )

    def _navigate_to_groups(self):
        """Navigate to groups page"""
        if self.groups_page:
            self.groups_page.refresh()
        self.navigation_callback(None, 1)

    def _handle_save(self, e):
        """Handle save button click"""
        group_data = {
            "name": self.form_fields['name'].value.strip() if self.form_fields['name'].value else "",
            "location": self.form_fields['location'].value.strip() if self.form_fields['location'].value else "",
            "price": self.form_fields['price'].value.strip() if self.form_fields['price'].value else "",
            "age_group": self.form_fields['age'].value.strip() if self.form_fields['age'].value else "",
            "teacher": self.form_fields['teacher'].value.strip() if self.form_fields['teacher'].value else "",
            "group_start_date": self.form_fields['start_date'].value.strip() if self.form_fields['start_date'].value else "",
            "day_of_week": self.form_fields['day_of_week'].value.strip() if self.form_fields['day_of_week'].value else "",
            "phone": self.form_fields['phone'].value.strip() if self.form_fields['phone'].value else "",
            "email": self.form_fields['email'].value.strip() if self.form_fields['email'].value else "",
        }
        
        # Validate form data
        is_valid, error_message = self.data_manager.validate_group_data(group_data)
        if not is_valid:
            # Navigate to groups page even on validation error
            self._navigate_to_groups()
            return
        
        # Save group
        success, message = self.data_manager.save_group(group_data)
        
        # Reset form and navigate to groups page regardless of success/failure
        self._reset_form()
        self._navigate_to_groups()

    def _handle_cancel(self, e):
        """Handle cancel button click"""
        self._navigate_to_groups()

    def _reset_form(self):
        """Reset form to initial state"""
        for key in self.form_state:
            self.form_state[key] = ''
            self.form_fields[key].value = ""
            self.form_fields[key].update()

    def get_view(self):
        return self.main_layout

    def save_group(self, e):
        """Legacy method - delegates to new handler"""
        self._handle_save(e)

    def go_back(self, e):
        """Legacy method - delegates to new handler""" 
        self._handle_cancel(e)
