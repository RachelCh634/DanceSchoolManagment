import flet as ft
from utils.groups_data_manager import GroupsDataManager
import re
from datetime import datetime


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

        # הגדרת שדות חובה
        self.required_fields = {
            'name': 'שם הקבוצה',
            'location': 'מיקום',
            'price': 'מחיר',
            'age': 'קבוצת גיל',
            'teacher': 'מורה/מדריך',
            'start_date': 'תאריך התחלה',
            'day_of_week': 'יום בשבוע'
        }

        # שגיאות ולידציה
        self.validation_errors = {}
        
        self.form_fields = self._create_form_fields()
        self.main_layout = self._render()

    def _create_form_fields(self):
        """Create styled form fields with modern React-like approach"""
        return {
            'name': self._create_text_field(
                label="שם הקבוצה *",
                hint="הכנס שם קבוצה",
                icon=ft.Icons.BADGE_OUTLINED,
                key='name',
                required=True
            ),
            'location': self._create_text_field(
                label="מיקום *",
                hint="מיקום הקבוצה",
                icon=ft.Icons.LOCATION_ON_OUTLINED,
                key='location',
                required=True
            ),
            'price': self._create_text_field(
                label="מחיר *",
                hint="מחיר לשיעור",
                icon=ft.Icons.PAYMENTS_OUTLINED,
                suffix="₪",
                keyboard_type=ft.KeyboardType.NUMBER,
                key='price',
                required=True
            ),
            'age': self._create_text_field(
                label="קבוצת גיל *",
                hint="טווח גילאים (לדוג' 6-8)",
                icon=ft.Icons.GROUPS_OUTLINED,
                key='age',
                required=True
            ),
            'teacher': self._create_text_field(
                label="מורה/מדריך *",
                hint="שם המורה או המדריך",
                icon=ft.Icons.PERSON_OUTLINE,
                key='teacher',
                required=True
            ),
            'start_date': self._create_text_field(
                label="תאריך התחלה *",
                hint="dd/mm/yyyy",
                icon=ft.Icons.DATE_RANGE_OUTLINED,
                key='start_date',
                required=True
            ),
            'day_of_week': self._create_text_field(
                label="יום בשבוע *",
                hint="לדוג' ראשון, שני, שלישי...",
                icon=ft.Icons.CALENDAR_VIEW_WEEK,
                key='day_of_week',
                required=True
            ),
            'phone': self._create_text_field(
                label="טלפון המורה",
                hint="מספר טלפון של המורה",
                icon=ft.Icons.PHONE,
                keyboard_type=ft.KeyboardType.PHONE,
                key='phone'
            ),
            'email': self._create_text_field(
                label="אימייל המורה",
                hint="כתובת אימייל של המורה",
                icon=ft.Icons.EMAIL_OUTLINED,
                keyboard_type=ft.KeyboardType.EMAIL,
                key='email'
            ),
        }

    def _create_text_field(self, label, hint, icon, key, suffix=None, keyboard_type=None, required=False):
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
            on_change=lambda e, field_key=key: self._handle_field_change(field_key, e.control.value),
            on_blur=lambda e, field_key=key: self._validate_field(field_key, e.control.value) if required else None
        )
        return field

    def _handle_field_change(self, key, value):
        """Handle field changes (React-like state management)"""
        self.form_state[key] = value
        # נקה שגיאות קודמות כשהמשתמש מתחיל להקליד
        if key in self.validation_errors:
            del self.validation_errors[key]
            self._update_field_style(key)

    def _validate_field(self, key, value):
        """Validate individual field"""
        error = None
        
        # בדיקת שדות חובה
        if key in self.required_fields and (not value or not value.strip()):
            error = f"{self.required_fields[key]} הוא שדה חובה"
        
        # ולידציות ספציפיות
        elif value and value.strip():
            if key == 'email' and value:
                if not self._is_valid_email(value):
                    error = "כתובת אימייל לא תקינה"
            
            elif key == 'phone' and value:
                if not self._is_valid_phone(value):
                    error = "מספר טלפון לא תקין"
            
            elif key == 'price':
                if not value.isdigit() or int(value) <= 0:
                    error = "המחיר חייב להיות מספר חיובי"
            
            elif key == 'start_date':
                if not self._is_valid_date(value):
                    error = "תאריך לא תקין (dd/mm/yyyy)"
            
            elif key == 'name':
                if len(value.strip()) < 2:
                    error = "שם הקבוצה חייב להכיל לפחות 2 תווים"
            
            elif key == 'teacher':
                if len(value.strip()) < 2:
                    error = "שם המורה חייב להכיל לפחות 2 תווים"
                    
            
        
        # עדכן את מצב השגיאה
        if error:
            self.validation_errors[key] = error
        elif key in self.validation_errors:
            del self.validation_errors[key]
        
        self._update_field_style(key)
        return error is None

    def _update_field_style(self, key):
        """Update field style based on validation state"""
        field = self.form_fields.get(key)
        if not field:
            return
        
        if key in self.validation_errors:
            # שדה עם שגיאה
            field.border_color = "#ef4444"
            field.focused_border_color = "#dc2626"
            field.error_text = self.validation_errors[key]
        else:
            # שדה תקין
            field.border_color = "#e1e7ef"
            field.focused_border_color = "#3b82f6"
            field.error_text = None
        
        try:
            field.update()
        except:
            pass

    def _is_valid_email(self, email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def _is_valid_phone(self, phone):
        """Validate Israeli phone number format"""
        # הסרת רווחים ומקפים
        phone = re.sub(r'[\s-]', '', phone)
        
        # בדיקת פורמטים ישראליים נפוצים
        patterns = [
            r'^0[2-9]\d{7,8}$',  # קווי בבית
            r'^05[0-9]\d{7}$',   # סלולר
            r'^1[5-9]\d{2,3}$',  # מספרים קצרים
            r'^\+972[2-9]\d{7,8}$',  # קוד בין-לאומי
        ]
        
        return any(re.match(pattern, phone) for pattern in patterns)

    def _is_valid_date(self, date_str):
        """Validate date format dd/mm/yyyy"""
        try:
            datetime.strptime(date_str, '%d/%m/%Y')
            return True
        except ValueError:
            return False

    def _validate_all_fields(self):
        """Validate all form fields"""
        self.validation_errors.clear()
        all_valid = True
        
        for key, value in self.form_state.items():
            field_value = value.strip() if value else ""
            if not self._validate_field(key, field_value):
                all_valid = False
        
        return all_valid

    def _show_validation_dialog(self):
        """Show validation errors dialog"""
        error_messages = []
        
        # הוסף שגיאות של שדות חובה
        for key, label in self.required_fields.items():
            if key in self.validation_errors:
                error_messages.append(f"• {self.validation_errors[key]}")
        
        # הוסף שגיאות אחרות
        for key, error in self.validation_errors.items():
            if key not in self.required_fields:
                error_messages.append(f"• {error}")
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(ft.Icons.ERROR_OUTLINE, color="#ef4444", size=28),
                ft.Text("שגיאות בטופס", size=20, weight=ft.FontWeight.BOLD, color="#ef4444")
            ], spacing=12),
            content=ft.Container(
                content=ft.Column([
                    ft.Text(
                        "יש לתקן את השגיאות הבאות:",
                        size=16,
                        color="#64748b",
                        weight=ft.FontWeight.W_500
                    ),
                    ft.Container(height=16),
                    ft.Column([
                        ft.Text(
                            error,
                            size=14,
                            color="#0f172a"
                        ) for error in error_messages[:10]  # הגבל ל-10 שגיאות
                    ], spacing=8),
                ], spacing=0),
                width=400,
                padding=ft.padding.all(20)
            ),
            actions=[
                ft.Container(
                    content=ft.TextButton(
                        "הבנתי",
                        on_click=lambda e: self._close_dialog(),
                        style=ft.ButtonStyle(
                            color="#3b82f6",
                            text_style=ft.TextStyle(
                                weight=ft.FontWeight.BOLD,
                                size=16
                            )
                        )
                    ),
                    padding=ft.padding.symmetric(horizontal=20, vertical=10)
                )
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
            shape=ft.RoundedRectangleBorder(radius=16),
            bgcolor="#ffffff",
            elevation=8
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def _close_dialog(self):
        """Close the dialog"""
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()

    def _show_success_dialog(self):
        """Show success dialog"""
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, color="#10b981", size=28),
                ft.Text("הצלחה!", size=20, weight=ft.FontWeight.BOLD, color="#10b981")
            ], spacing=12),
            content=ft.Container(
                content=ft.Text(
                    "הקבוצה נשמרה בהצלחה במערכת",
                    size=16,
                    color="#64748b",
                    text_align=ft.TextAlign.CENTER
                ),
                width=300,
                padding=ft.padding.all(20)
            ),
            actions=[
                ft.Container(
                    content=ft.ElevatedButton(
                        "אישור",
                        on_click=lambda e: self._handle_success_dialog_close(),
                        style=ft.ButtonStyle(
                            bgcolor="#10b981",
                            color="white",
                            text_style=ft.TextStyle(
                                weight=ft.FontWeight.BOLD,
                                size=16
                            ),
                            shape=ft.RoundedRectangleBorder(radius=8)
                        )
                    ),
                    padding=ft.padding.symmetric(horizontal=20, vertical=10)
                )
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
            shape=ft.RoundedRectangleBorder(radius=16),
            bgcolor="#ffffff",
            elevation=8
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def _handle_success_dialog_close(self):
        """Handle success dialog close"""
        self._close_dialog()
        self._reset_form()
        self._navigate_to_groups()

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
                            "מלא את הפרטים הנדרשים ליצירת קבוצה חדשה במערכת. שדות עם * הם חובה",
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
                    col={"xs": 12, "sm": 12, "md": 6},
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
        """Handle save button click with validation"""
        # עדכן את form_state עם הערכים הנוכחיים
        for key, field in self.form_fields.items():
            self.form_state[key] = field.value or ""
        
        # בצע ולידציה מלאה
        if not self._validate_all_fields():
            self._show_validation_dialog()
            return
        
        # הכן נתונים לשמירה
        price_value = self.form_state['price'].strip()
        try:
            price_int = int(price_value) if price_value and price_value.isdigit() else 0
        except (ValueError, TypeError):
            price_int = 0
        
        group_data = {
            "name": self.form_state['name'].strip(),
            "location": self.form_state['location'].strip(),
            "price": price_int,
            "age_group": self.form_state['age'].strip(),
            "teacher": self.form_state['teacher'].strip(),
            "group_start_date": self.form_state['start_date'].strip(),
            "day_of_week": self.form_state['day_of_week'].strip(),
            "teacher_phone": self.form_state['phone'].strip(),
            "teacher_email": self.form_state['email'].strip(),
        }
        
        # Debug: הדפסת הנתונים שנשלחים
        print("Group data to save:")
        for key, value in group_data.items():
            print(f"{key}: '{value}' (type: {type(value)})")
        
        # Validate form data with data manager
        is_valid, error_message = self.data_manager.validate_group_data(group_data)
        if not is_valid:
            print(f"Data manager validation error: {error_message}")
            self._show_error_dialog(f"שגיאה בוולידציה: {error_message}")
            return
        
        # Save group
        success, message = self.data_manager.save_group(group_data)
        
        if success:
            print("Group saved successfully")
            self._show_success_dialog()
        else:
            print(f"Save error: {message}")
            self._show_error_dialog(f"שגיאה בשמירה: {message}")

    def _show_error_dialog(self, message):
        """Show error dialog"""
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(ft.Icons.ERROR_OUTLINE, color="#ef4444", size=28),
                ft.Text("שגיאה", size=20, weight=ft.FontWeight.BOLD, color="#ef4444")
            ], spacing=12),
            content=ft.Container(
                content=ft.Text(
                    message,
                    size=16,
                    color="#64748b",
                    text_align=ft.TextAlign.CENTER
                ),
                width=350,
                padding=ft.padding.all(20)
            ),
            actions=[
                ft.Container(
                    content=ft.TextButton(
                        "הבנתי",
                        on_click=lambda e: self._close_dialog(),
                        style=ft.ButtonStyle(
                            color="#ef4444",
                            text_style=ft.TextStyle(
                                weight=ft.FontWeight.BOLD,
                                size=16
                            )
                        )
                    ),
                    padding=ft.padding.symmetric(horizontal=20, vertical=10)
                )
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
            shape=ft.RoundedRectangleBorder(radius=16),
            bgcolor="#ffffff",
            elevation=8
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def _handle_cancel(self, e):
        """Handle cancel button click"""
        self._navigate_to_groups()

    def _reset_form(self):
        """Reset form to initial state"""
        for key in self.form_state:
            self.form_state[key] = ''
            if key in self.form_fields:
                self.form_fields[key].value = ""
                self.form_fields[key].error_text = None
                self.form_fields[key].border_color = "#e1e7ef"
                self.form_fields[key].focused_border_color = "#3b82f6"
                try:
                    self.form_fields[key].update()
                except:
                    pass
        
        self.validation_errors.clear()

    def get_view(self):
        return self.main_layout

    def save_group(self, e):
        """Legacy method - delegates to new handler"""
        self._handle_save(e)

    def go_back(self, e):
        """Legacy method - delegates to new handler""" 
        self._handle_cancel(e)