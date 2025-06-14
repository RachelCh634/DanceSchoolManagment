import json
import os
import flet as ft
from typing import Dict, Any
from attendance_table_view import AttendanceTableView 
import datetime


class AttendanceCheckBox:
    def __init__(self, date: str, student_id: str, parent_page, is_checked: bool = False):
        self.date = date
        self.student_id = student_id
        self.parent_page = parent_page
        self.is_checked = is_checked
        
    def create_checkbox(self):
        """Create the modern checkbox widget with animations"""
        def on_click(e):
            self.is_checked = not self.is_checked
            self.parent_page.update_attendance(self.date, self.student_id, self.is_checked)
            # Update the checkbox appearance with animation
            e.control.content = self.get_checkbox_content()
            e.control.update()
        
        return ft.Container(
            content=self.get_checkbox_content(),
            width=40,
            height=40,
            border_radius=20,
            on_click=on_click,
            animate=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            animate_scale=ft.Animation(200, ft.AnimationCurve.BOUNCE_OUT),
            ink=True,
            tooltip="לחץ כדי לשנות נוכחות",
        )
    
    def get_checkbox_content(self):
        """Get the modern checkbox content based on state"""
        if self.is_checked:
            return ft.Container(
                content=ft.Icon(
                    ft.Icons.CHECK_ROUNDED,
                    color=ft.Colors.WHITE,
                    size=24,
                ),
                bgcolor=ft.Colors.GREEN_500,
                border_radius=20,
                alignment=ft.alignment.center,
            )
        else:
            return ft.Container(
                content=ft.Icon(
                    ft.Icons.CLOSE_ROUNDED,
                    color=ft.Colors.WHITE,
                    size=24,
                ),
                bgcolor=ft.Colors.RED_500,
                border_radius=20,
                alignment=ft.alignment.center,
            )

class GroupAttendancePage:
    def __init__(self, page: ft.Page, navigation_handler=None, group: Dict[str, Any] = None):
        self.page = page
        self.navigation_handler = navigation_handler
        self.group = group or {}
        self.attendance_data = {}
        self.students = []
        
        # UI components
        self.attendance_table = None
        self.checkboxes = {}
        self.main_content = None
        
        # Load data
        self.load_attendance()
        self.load_students()

    def load_attendance(self):
        """Load attendance data from JSON file"""
        path = f"attendances/attendance_{self.group.get('id', '')}.json"
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self.attendance_data = json.load(f)
            except Exception as e:
                print(f"Error loading attendance: {e}")
                self.attendance_data = {}
        else:
            self.attendance_data = {}

    def load_students(self):
        """Load students for this group"""
        try:
            if os.path.exists("data/students.json"):
                with open("data/students.json", "r", encoding="utf-8") as f:
                    students_data = json.load(f)
                    for s in students_data.get("students", []):
                        if s.get("group", "").strip() == self.group.get("name", "").strip():
                            self.students.append({"id": s["id"], "name": s["name"]})
        except Exception as e:
            print(f"Error loading students: {e}")

    def save_attendance(self):
        """Save attendance data to JSON file"""
        try:
            os.makedirs("attendances", exist_ok=True)
            path = f"attendances/attendance_{self.group.get('id', '')}.json"
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.attendance_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving attendance: {e}")

    def update_attendance(self, date: str, student_id: str, is_present: bool):
        """Update attendance data"""
        if date not in self.attendance_data:
            self.attendance_data[date] = {}
        
        self.attendance_data[date][str(student_id)] = is_present
        self.save_attendance()

    def create_modern_card(self, content, bgcolor=None, padding=20, blur=True):
        """Create a modern glassmorphism card"""
        return ft.Container(
            content=content,
            bgcolor=bgcolor or ft.Colors.with_opacity(0.9, ft.Colors.WHITE),
            border_radius=16,
            padding=ft.padding.all(padding),
            border=ft.border.all(1, ft.Colors.with_opacity(0.2, ft.Colors.GREY_300)),
            animate=ft.Animation(500, ft.AnimationCurve.EASE_OUT),
        )

    def create_gradient_background(self):
        """Create gradient background with warmer colors"""
        return ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[
                    ft.Colors.ORANGE_50,
                    ft.Colors.PINK_50,
                    ft.Colors.PURPLE_50,
                    ft.Colors.DEEP_PURPLE_50,
                ]
            ),
            expand=True,
        )

    def create_header_card(self):
        """Create modern clean header card - RIGHT ALIGNED"""
        header_content = ft.Column([
            ft.Row([
                ft.Column([
                    ft.Text(
                        "ניהול נוכחות",
                        size=24,
                        weight=ft.FontWeight.W_700,
                        color=ft.Colors.GREY_800,
                        rtl=True
                    ),
                    ft.Text(
                        f"קבוצת {self.group.get('name', '')}",
                        size=14,
                        color=ft.Colors.GREY_500,
                        rtl=True
                    ),
                ], spacing=2, alignment=ft.CrossAxisAlignment.END),
                ft.Container(width=12),
                ft.Container(
                    content=ft.Icon(ft.Icons.HOW_TO_REG, size=28, color=ft.Colors.BLUE_600),
                    bgcolor=ft.Colors.BLUE_50,
                    border_radius=14,
                    padding=ft.padding.all(12),
                ),
            ], alignment=ft.alignment.center_right),
        ], 
        horizontal_alignment=ft.CrossAxisAlignment.END,
        spacing=0
        )
        
        return ft.Container(
            content=header_content,
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, ft.Colors.GREY_200),
            border_radius=16,
            padding=ft.padding.all(24),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=20,
                color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                offset=ft.Offset(0, 4),
            ),
        )

    def create_stats_card(self):
        """Create clean centered statistics card"""
        dates = list(self.attendance_data.keys())
        total_dates = len(dates)
        total_students = len(self.students)
        
        return ft.Container(
            content=ft.Row([
                # Total dates card
                ft.Container(
                    content=ft.Column([
                        ft.Container(
                            content=ft.Icon(ft.Icons.CALENDAR_TODAY_OUTLINED, size=20, color=ft.Colors.BLUE_600),
                            bgcolor=ft.Colors.BLUE_50,
                            border_radius=8,
                            padding=ft.padding.all(8),
                        ),
                        ft.Container(height=8),
                        ft.Text(str(total_dates), size=20, weight=ft.FontWeight.W_700, color=ft.Colors.GREY_800),
                        ft.Text("תאריכים", size=12, color=ft.Colors.GREY_500, rtl=True),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                    bgcolor=ft.Colors.WHITE,
                    border=ft.border.all(1, ft.Colors.GREY_200),
                    padding=ft.padding.all(16),
                    border_radius=12,
                    width=120,
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=8,
                        color=ft.Colors.with_opacity(0.06, ft.Colors.BLACK),
                        offset=ft.Offset(0, 2),
                    ),
                ),
                
                ft.Container(width=16),
                
                # Total students card
                ft.Container(
                    content=ft.Column([
                        ft.Container(
                            content=ft.Icon(ft.Icons.PEOPLE_OUTLINE, size=20, color=ft.Colors.PURPLE_600),
                            bgcolor=ft.Colors.PURPLE_50,
                            border_radius=8,
                            padding=ft.padding.all(8),
                        ),
                        ft.Container(height=8),
                        ft.Text(str(total_students), size=20, weight=ft.FontWeight.W_700, color=ft.Colors.GREY_800),
                        ft.Text("תלמידים", size=12, color=ft.Colors.GREY_500, rtl=True),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                    bgcolor=ft.Colors.WHITE,
                    border=ft.border.all(1, ft.Colors.GREY_200),
                    padding=ft.padding.all(16),
                    border_radius=12,
                    width=120,
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=8,
                        color=ft.Colors.with_opacity(0.06, ft.Colors.BLACK),
                        offset=ft.Offset(0, 2),
                    ),
                ),
            ], 
            alignment=ft.MainAxisAlignment.CENTER,
            tight=True
            ),
            padding=ft.padding.symmetric(vertical=16),
            alignment=ft.alignment.center,
        )

    def create_modern_button(self, text, icon, on_click, color=ft.Colors.BLUE_600, width=None):
        """Create clean modern button"""
        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, size=16, color=ft.Colors.WHITE),
                ft.Container(width=8),
                ft.Text(text, size=14, weight=ft.FontWeight.W_500, color=ft.Colors.WHITE, rtl=True),
            ], 
            alignment=ft.MainAxisAlignment.CENTER,
            tight=True
            ),
            bgcolor=color,
            border_radius=8,
            padding=ft.padding.symmetric(horizontal=16, vertical=12),
            width=width or 140,
            on_click=on_click,
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
            ink=True,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.15, color),
                offset=ft.Offset(0, 2),
            ),
        )

    def create_actions_card(self):
        """Create clean centered actions section"""
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.ADD, size=18, color=ft.Colors.WHITE),
                        ft.Container(width=6),
                        ft.Text("הוסף תאריך", size=14, weight=ft.FontWeight.W_500, color=ft.Colors.WHITE, rtl=True),
                    ], 
                    alignment=ft.MainAxisAlignment.CENTER,
                    tight=True,
                    spacing=0
                    ),
                    bgcolor=ft.Colors.BLUE_600,
                    border_radius=8,
                    padding=ft.padding.symmetric(horizontal=16, vertical=12),
                    width=140,
                    on_click=self.show_add_date_dialog,
                    animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
                    ink=True,
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=8,
                        color=ft.Colors.with_opacity(0.15, ft.Colors.BLUE_600),
                        offset=ft.Offset(0, 2),
                    ),
                ),
                
                ft.Container(width=12),
            ], 
            alignment=ft.MainAxisAlignment.CENTER,
            tight=True
            ),
            padding=ft.padding.symmetric(vertical=16),
            alignment=ft.alignment.center,
        )

    def show_add_date_dialog(self, e):
        """Show enhanced add date dialog with fixed scrolling"""
        selected_date = None
        
        date_display = ft.Text(
            "לא נבחר תאריך",
            size=14,
            color=ft.Colors.GREY_500,
            rtl=True,
        )
        
                # Error message container
        error_message = ft.Container(
            content=ft.Row([
                ft.Text("", size=12, color=ft.Colors.RED_500, rtl=True),
                ft.Container(width=8),
                ft.Icon(ft.Icons.ERROR_OUTLINE, size=16, color=ft.Colors.RED_500),
            ], alignment=ft.MainAxisAlignment.END),  # הזזה לימין
            visible=False,
            bgcolor=ft.Colors.RED_50,
            border=ft.border.all(1, ft.Colors.RED_200),
            border_radius=8,
            padding=ft.padding.all(12),
            margin=ft.margin.only(top=8),
            alignment=ft.alignment.center_right,  # יישור הקונטיינר לימין
        )
        
        def show_error(message):
            error_message.content.controls[0].value = message 
            error_message.visible = True
            error_message.update()
        
        def hide_error():
            error_message.visible = False
            error_message.update()
        
        def handle_date_change(e):
            nonlocal selected_date
            selected_date = e.control.value
            date_display.value = f"תאריך נבחר: {selected_date.strftime('%d/%m/%Y')}"
            date_display.color = ft.Colors.GREY_700
            date_display.update()
            hide_error()
        
        def handle_date_dismiss(e):
            pass
        
        def open_date_picker(e):
            hide_error()
            self.page.open(
                ft.DatePicker(
                    first_date=datetime.datetime(year=2020, month=1, day=1),
                    last_date=datetime.datetime(year=2030, month=12, day=31),
                    on_change=handle_date_change,
                    on_dismiss=handle_date_dismiss,
                )
            )
        
        # Compact date picker button
        date_picker_button = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.CALENDAR_TODAY, size=18, color=ft.Colors.BLUE_600),
                ft.Container(width=6),
                ft.Text("בחר תאריך", size=14, weight=ft.FontWeight.W_500, rtl=True),
            ], tight=True, alignment=ft.MainAxisAlignment.CENTER),
            bgcolor=ft.Colors.BLUE_50,
            border=ft.border.all(1, ft.Colors.BLUE_300),
            border_radius=8,
            padding=ft.padding.symmetric(horizontal=12, vertical=8),
            on_click=open_date_picker,
            ink=True,
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
            width=140,
        )
        
        # Create attendance selection for each student
        student_attendance = {}
        attendance_rows = []
        
        if self.students:
            for student in self.students:
                student_attendance[student["id"]] = False
                
                def create_toggle_click(student_id):
                    def toggle_attendance(e):
                        student_attendance[student_id] = not student_attendance[student_id]
                        is_present = student_attendance[student_id]
                        
                        if is_present:
                            new_icon = ft.Icon(ft.Icons.CHECK_CIRCLE, size=20, color=ft.Colors.GREEN_600)
                            e.control.tooltip = "נוכח - לחץ לשינוי"
                        else:
                            new_icon = ft.Icon(ft.Icons.CANCEL, size=20, color=ft.Colors.BLUE_600)
                            e.control.tooltip = "נעדר - לחץ לשינוי"
                        
                        e.control.content = new_icon
                        e.control.update()
                        
                    return toggle_attendance
                
                student_row = ft.Container(
                    content=ft.Row([
                        ft.Text(
                            student["name"],
                            size=14,
                            color=ft.Colors.GREY_700,
                            weight=ft.FontWeight.W_500,
                            rtl=True,
                        ),
                        ft.Container(
                            content=ft.Icon(ft.Icons.CANCEL, size=20, color=ft.Colors.BLUE_600),
                            padding=ft.padding.all(6),
                            width=35,
                            height=35,
                            alignment=ft.alignment.center,
                            on_click=create_toggle_click(student["id"]),
                            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
                            tooltip="נעדר - לחץ לשינוי",
                            ink=True,
                            border_radius=20,
                        ),
                    ], 
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    rtl=True,
                    ),
                    padding=ft.padding.symmetric(horizontal=12, vertical=6),
                    border_radius=6,
                    border=ft.border.all(1, ft.Colors.GREY_200),
                    margin=ft.margin.only(bottom=4),
                )
                attendance_rows.append(student_row)

        def on_confirm(e):
            try:
                if selected_date:
                    date_str = selected_date.strftime('%d/%m/%Y')
                    if date_str not in self.attendance_data:
                        self.attendance_data[date_str] = {}
                        
                        for student_id, is_present in student_attendance.items():
                            self.attendance_data[date_str][str(student_id)] = is_present
                        
                        self.save_attendance()
                        self.page.close(dlg)
                        self.refresh_view()
                        self.show_success_snackbar(f"תאריך {date_str} נוסף בהצלחה!")
                    else:
                        show_error("התאריך הזה כבר קיים במערכת!")
                else:
                    show_error("אנא בחרי תאריך")
            except Exception as ex:
                print(f"Error in add_date: {ex}")
                show_error("שגיאה בהוספת התאריך")

        def on_cancel(e):
            self.page.close(dlg)

        # Create dialog content with RTL alignment
        content_items = [
            # Header - RTL aligned
            ft.Container(
                content=ft.Row([
                    ft.Column([
                        ft.Text("הוסף תאריך חדש", size=18, weight=ft.FontWeight.W_700, color=ft.Colors.GREY_800, rtl=True),
                        ft.Text("בחר תאריך וסמן נוכחות", size=12, color=ft.Colors.GREY_500, rtl=True),
                    ], spacing=4, alignment=ft.CrossAxisAlignment.END),
                    ft.Container(width=12),
                    ft.Container(
                        content=ft.Icon(ft.Icons.EVENT_OUTLINED, size=28, color=ft.Colors.BLUE_600),
                        bgcolor=ft.Colors.BLUE_50,
                        border_radius=14,
                        padding=ft.padding.all(10),
                    ),
                ], alignment=ft.MainAxisAlignment.END),
                margin=ft.margin.only(bottom=20),
            ),
            
            # Date picker section - RTL aligned
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text("בחירת תאריך:", size=14, weight=ft.FontWeight.W_600, color=ft.Colors.GREY_700, rtl=True),
                    ], alignment=ft.MainAxisAlignment.END),
                    ft.Container(height=8),
                    ft.Row([
                        date_picker_button,
                    ], alignment=ft.MainAxisAlignment.END),
                    ft.Container(height=8),
                    ft.Row([
                        date_display,
                    ], alignment=ft.MainAxisAlignment.END),
                    error_message,
                ]),
                margin=ft.margin.only(bottom=20),
            ),
            
            # Students section header - RTL aligned
            ft.Row([
                ft.Text("סמן נוכחות תלמידות:", size=14, weight=ft.FontWeight.W_600, color=ft.Colors.GREY_700, rtl=True),
            ], alignment=ft.MainAxisAlignment.END),
            ft.Container(height=12),
        ]
        
        # FIXED: Create scrollable students list with proper height
        if attendance_rows:
            students_scroll_container = ft.Container(
                content=ft.Column(
                    controls=attendance_rows,
                    spacing=0,
                    scroll=ft.ScrollMode.AUTO,  # Enable scroll
                ),
                height=min(250, max(150, len(attendance_rows) * 45)),  # Dynamic height with min/max
                bgcolor=ft.Colors.WHITE,
                border_radius=8,
                border=ft.border.all(1, ft.Colors.GREY_200),
                padding=ft.padding.all(8),
            )
            content_items.append(students_scroll_container)

        # FIXED: Create main content with proper scrolling
        content = ft.Container(
            content=ft.Column(
                controls=content_items,
                horizontal_alignment=ft.CrossAxisAlignment.END,
                tight=True,
                spacing=0,
                # scroll=ft.ScrollMode.AUTO,  # Enable main scroll
            ),
            width=420,
            height=min(500, 200 + (len(attendance_rows) * 45) if attendance_rows else 300),  # Dynamic dialog height
        )

        # Clean action buttons
        actions = [
            ft.Container(
                content=ft.Row([
                    ft.TextButton(
                        "ביטול", 
                        on_click=on_cancel,
                        style=ft.ButtonStyle(
                            color=ft.Colors.GREY_600,
                            padding=ft.padding.symmetric(horizontal=16, vertical=8),
                        )
                    ),
                    ft.Container(width=16),  # רווח בין הכפתורים
                    ft.ElevatedButton(
                        "הוסף תאריך",
                        on_click=on_confirm,
                        bgcolor=ft.Colors.BLUE_600,
                        color=ft.Colors.WHITE,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            padding=ft.padding.symmetric(horizontal=16, vertical=8),
                            elevation=0,
                        )
                    ),
                ], alignment=ft.MainAxisAlignment.CENTER),  # ריכוז הכפתורים
                margin=ft.margin.only(top=40),  # רווח מלמעלה
            )
        ]


        dlg = ft.AlertDialog(
            modal=True,
            content=content,
            actions=actions,
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=16),
            content_padding=ft.padding.all(20),
        )
        
        self.page.open(dlg)

    def refresh_view(self):
        """Refresh the entire view"""
        try:
            # Reload data
            self.load_data()
            
            # Recreate the main content
            if self.main_content:
                new_content = self.create_page_content()
                self.main_content.content = new_content
                self.main_content.update()
                
        except Exception as e:
            print(f"Error refreshing view: {e}")
            self.show_error_snackbar("שגיאה ברענון הנתונים")

    def create_table_header(self):
        """Create modern table header"""
        headers = []
        
        # Date header
        headers.append(
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.CALENDAR_TODAY, size=16, color=ft.Colors.WHITE),
                    ft.Container(width=8),
                    ft.Text("תאריך", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE, rtl=True),
                ], alignment=ft.MainAxisAlignment.CENTER),
                bgcolor=ft.Colors.DEEP_PURPLE_600,
                padding=ft.padding.all(16),
                width=150,
                border_radius=ft.BorderRadius(12, 0, 0, 12) if len(self.students) > 0 else 12,
            )
        )
        
        # Student headers
        for i, student in enumerate(self.students):
            is_last = (i == len(self.students) - 1)
            headers.append(
                ft.Container(
                    content=ft.Text(
                        student["name"], 
                        size=14, 
                        weight=ft.FontWeight.BOLD, 
                        color=ft.Colors.WHITE,
                        text_align=ft.TextAlign.CENTER,
                        rtl=True
                    ),
                    bgcolor=ft.Colors.DEEP_PURPLE_600,
                    padding=ft.padding.all(16),
                    width=130,
                    border_radius=ft.BorderRadius(0, 12 if is_last else 0, 12 if is_last else 0, 0),
                )
            )
        
        return ft.Row(headers, spacing=1)

    def create_table_row(self, date: str):
        """Create React-style table row"""
        row_cells = [
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.EDIT_OUTLINED, size=14, color=ft.Colors.BLUE_400),
                    ft.Container(width=8),
                    ft.Text(
                        date, 
                        size=14, 
                        color=ft.Colors.GREY_700,
                        weight=ft.FontWeight.W_500
                    ),
                ], alignment=ft.MainAxisAlignment.START),
                width=140,
                padding=ft.padding.symmetric(horizontal=16, vertical=12),
                on_click=lambda e, d=date: self.show_date_options(d),
                ink=True,
                border_radius=8,
                tooltip="לחץ לעריכה",
            )
        ]
        
        # Add attendance cells
        for student in self.students:
            is_present = self.attendance_data.get(date, {}).get(str(student["id"]), False)
            row_cells.append(
                ft.Container(
                    content=self.create_status_toggle(is_present, date, student["id"]),
                    width=120,
                    padding=ft.padding.symmetric(horizontal=12, vertical=12),
                    alignment=ft.alignment.center,
                )
            )
        
        return ft.Container(
            content=ft.Row(row_cells, spacing=0),
            bgcolor=ft.Colors.WHITE,
            border=ft.border.only(bottom=ft.BorderSide(1, ft.Colors.GREY_100)),
            on_hover=self.on_row_hover,
        )

    def create_modern_data_table(self):
        """Create modern React-style table with clean design"""
        dates = list(self.attendance_data.keys())
        
        if not dates or not self.students:
            return self.create_empty_table_state()
        
        # Create table header
        header_row = self.create_table_header()
        
        # Create table rows - FIXED: Sort oldest to newest (oldest at bottom)
        table_rows = []
        sorted_dates = self.sort_dates_newest_first(dates)
        
        for date in sorted_dates:
            table_rows.append(self.create_table_row(date))
        
        # Create the table container
        table_content = ft.Column([
            header_row,
            ft.Container(height=1, bgcolor=ft.Colors.GREY_200),
            ft.Column(table_rows, spacing=0),
        ], spacing=0)
        
        return ft.Container(
            content=table_content,
            bgcolor=ft.Colors.WHITE,
            border_radius=16,
            border=ft.border.all(1, ft.Colors.GREY_200),
            padding=ft.padding.all(0),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=20,
                color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                offset=ft.Offset(0, 4),
            ),
        )

    def sort_dates_newest_first(self, dates):
        """Sort dates from newest to oldest with better parsing"""
        try:
            import datetime
            date_objects = []
            
            for date_str in dates:
                try:
                    # נסה פורמטים שונים
                    date_obj = None
                    
                    # נסה DD/MM/YYYY
                    if '/' in date_str and len(date_str.split('/')) == 3:
                        parts = date_str.split('/')
                        if len(parts[0]) <= 2 and len(parts[1]) <= 2 and len(parts[2]) == 4:
                            day, month, year = parts
                            date_obj = datetime.datetime(int(year), int(month), int(day))
                    
                    # נסה DD-MM-YYYY
                    elif '-' in date_str and len(date_str.split('-')) == 3:
                        parts = date_str.split('-')
                        if len(parts[0]) <= 2 and len(parts[1]) <= 2 and len(parts[2]) == 4:
                            day, month, year = parts
                            date_obj = datetime.datetime(int(year), int(month), int(day))
                    
                    # נסה YYYY-MM-DD
                    elif '-' in date_str and len(date_str.split('-')) == 3:
                        parts = date_str.split('-')
                        if len(parts[0]) == 4 and len(parts[1]) <= 2 and len(parts[2]) <= 2:
                            year, month, day = parts
                            date_obj = datetime.datetime(int(year), int(month), int(day))
                    
                    if date_obj:
                        date_objects.append((date_obj, date_str))
                    else:
                        # אם לא הצלחנו לפרסר, שים בסוף
                        date_objects.append((datetime.datetime(1900, 1, 1), date_str))
                        print(f"Could not parse date: {date_str}")
                        
                except Exception as e:
                    print(f"Error parsing date {date_str}: {e}")
                    # אם יש שגיאה, שים בסוף
                    date_objects.append((datetime.datetime(1900, 1, 1), date_str))
            
            # מיון לפי תאריך (החדש ביותר ראשון)
            date_objects.sort(key=lambda x: x[0], reverse=True)
            
            # החזר רק את המחרוזות
            sorted_dates = [date_str for _, date_str in date_objects]
            
            print(f"Original dates: {dates}")
            print(f"Sorted dates: {sorted_dates}")
            
            return sorted_dates
            
        except Exception as e:
            print(f"Error in sort_dates_newest_first: {e}")
            # במקרה של שגיאה, החזר מיון פשוט
            return sorted(dates, reverse=True)

    def refresh_table(self):
        """Refresh the table data and view - improved version"""
        try:
            print("Refreshing table...")
            
            # Reload data from files
            self.load_data()
            
            # Recreate the entire page content
            if hasattr(self, 'main_content') and self.main_content:
                new_content = self.create_page_content()
                self.main_content.content = new_content
                self.main_content.update()
                print("Table refreshed successfully")
            else:
                print("main_content not found")
                
        except Exception as e:
            print(f"Error refreshing table: {e}")
            self.show_error_snackbar("שגיאה ברענון הטבלה")



    def create_attendance_table_card(self):
        """Create modern attendance table using AttendanceTableView"""
        dates = list(self.attendance_data.keys())
        
        if not dates and not self.students:
            # Modern empty state
            empty_content = ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.EVENT_NOTE_OUTLINED, size=80, color=ft.Colors.GREY_300),
                    ft.Container(height=16),
                    ft.Text(
                        "אין תאריכים או תלמידים להצגה",
                        size=20,
                        weight=ft.FontWeight.W_500,
                        color=ft.Colors.GREY_600,
                        text_align=ft.TextAlign.CENTER,
                        rtl=True
                    ),
                    ft.Container(height=8),
                    ft.Text(
                        "הוסף תאריך חדש כדי להתחיל",
                        size=16,
                        color=ft.Colors.GREY_500,
                        text_align=ft.TextAlign.CENTER,
                        rtl=True
                    ),
                ], 
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0
                ),
                padding=ft.padding.all(60),
                alignment=ft.alignment.center,
            )
            return self.create_modern_card(empty_content)
        
        # יצירת הטבלה החדשה
        table_view = AttendanceTableView(self.page, self.navigation_handler, self.group)
        
        # יצירת כותרת לטבלה
        table_header = ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.TABLE_CHART, size=24, color=ft.Colors.DEEP_PURPLE_600),
                ft.Container(width=8),
                ft.Text(
                    "טבלת נוכחות",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.DEEP_PURPLE_600,
                    rtl=True
                ),
            ]),
            ft.Container(height=8),
            ft.Text(
                "לחץ על התאריך כדי לערוך או למחוק אותו",
                size=14,
                color=ft.Colors.GREY_500,
                rtl=True,
                italic=True
            ),
            ft.Container(height=16),
        ])

        # שילוב הכותרת עם הטבלה
        table_content = ft.Column([
            table_header,
            ft.Container(
                content=table_view.create_modern_data_table(),
                expand=True,
            )
        ], spacing=0, tight=True)

        return self.create_modern_card(table_content)

    def show_modern_dialog(self, title: str, content, actions):
        """Show modern styled dialog - CORRECT VERSION"""
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(title, rtl=True, size=20, weight=ft.FontWeight.BOLD),
            content=content,
            actions=actions,
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print(f"Dialog {title} dismissed"),
        )
        
        # ✅ הדרך הנכונה!
        self.page.open(dialog)

    def add_new_date(self, e):
        """Show modern add date dialog - CORRECTED VERSION"""
        date_input = ft.TextField(
            hint_text="DD/MM/YYYY",
            width=250,
            text_align=ft.TextAlign.CENTER,
            border_radius=12,
            bgcolor=ft.Colors.GREY_50,
            autofocus=True,
        )

        def on_confirm(e):
            if date_input.value and date_input.value.strip():
                new_date = date_input.value.strip()
                if new_date not in self.attendance_data:
                    self.attendance_data[new_date] = {}
                    for student in self.students:
                        self.attendance_data[new_date][str(student["id"])] = False
                    
                    self.save_attendance()
                    self.page.close(dlg)  # ✅ סגור דיאלוג
                    self.refresh_page()
                    self.show_success_snackbar(f"התאריך {new_date} נוסף בהצלחה!")
                else:
                    self.show_error_snackbar("התאריך הזה כבר קיים!")
            else:
                self.show_error_snackbar("אנא הכנס תאריך!")

        def on_cancel(e):
            self.page.close(dlg)  # ✅ סגור דיאלוג

        content = ft.Column([
            ft.Icon(ft.Icons.CALENDAR_TODAY, size=48, color=ft.Colors.DEEP_PURPLE_500),
            ft.Container(height=16),
            ft.Text("הכנס תאריך חדש:", rtl=True, size=16),
            ft.Container(height=8),
            date_input
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, tight=True)

        actions = [
            ft.TextButton("ביטול", on_click=on_cancel),
            ft.ElevatedButton(
                "אישור", 
                on_click=on_confirm,
                bgcolor=ft.Colors.DEEP_PURPLE_500,
                color=ft.Colors.WHITE,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
            ),
        ]

        # ✅ יצירת הדיאלוג
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("הוסף תאריך חדש", rtl=True, size=20, weight=ft.FontWeight.BOLD),
            content=content,
            actions=actions,
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        # ✅ פתיחת הדיאלוג בדרך הנכונה!
        self.page.open(dlg)


    def show_context_menu_dialog(self, date: str):
        """Show modern context menu for date - CORRECTED VERSION"""
        def edit_date(e):
            self.page.close(dlg)
            self.edit_date_dialog(date)

        def delete_date(e):
            self.page.close(dlg)
            self.delete_date_dialog(date)

        def close_menu(e):
            self.page.close(dlg)

        content = ft.Column([
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.EDIT, color=ft.Colors.DEEP_PURPLE_600),
                    ft.Container(width=12),
                    ft.Text("ערוך תאריך", rtl=True, size=16),
                ]),
                padding=ft.padding.all(12),
                on_click=edit_date,
                border_radius=8,
                ink=True,
                bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.DEEP_PURPLE_600),
            ),
            ft.Container(height=8),
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.DELETE, color=ft.Colors.RED_600),
                    ft.Container(width=12),
                    ft.Text("מחק תאריך", rtl=True, size=16),
                ]),
                padding=ft.padding.all(12),
                on_click=delete_date,
                border_radius=8,
                ink=True,
                bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.RED_600),
            ),
        ], tight=True, spacing=0)

        actions = [ft.TextButton("ביטול", on_click=close_menu)]

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"פעולות עבור {date}", rtl=True, size=20, weight=ft.FontWeight.BOLD),
            content=content,
            actions=actions,
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        self.page.open(dlg)  # ✅ הדרך הנכונה!

    def edit_date_dialog(self, current_date: str):
        """Show edit date dialog - FIXED VERSION"""
        date_input = ft.TextField(
            value=current_date,
            width=250,
            text_align=ft.TextAlign.CENTER,
            border_radius=12,
            bgcolor=ft.Colors.GREY_50,
            border_color=ft.Colors.DEEP_PURPLE_200,
            focused_border_color=ft.Colors.DEEP_PURPLE_500,
            text_size=16,
        )

        def on_confirm(e):
            try:
                new_date = date_input.value.strip() if date_input.value else ""
                if new_date and new_date != current_date:
                    if new_date not in self.attendance_data:
                        # Move data from old date to new date
                        self.attendance_data[new_date] = self.attendance_data.pop(current_date)
                        self.save_attendance()
                        self.close_dialog()
                        self.refresh_page()
                        self.show_success_snackbar(f"התאריך עודכן ל-{new_date}")
                    else:
                        self.show_error_snackbar("התאריך הזה כבר קיים!")
                else:
                    self.show_error_snackbar("אנא הכנס תאריך תקין!")
            except Exception as ex:
                print(f"Error in edit_date: {ex}")
                self.show_error_snackbar("שגיאה בעריכת התאריך")

        def on_cancel(e):
            self.close_dialog()

        content = ft.Column([
            ft.Icon(ft.Icons.EDIT_CALENDAR, size=48, color=ft.Colors.DEEP_PURPLE_500),
            ft.Container(height=16),
            ft.Text("ערוך את התאריך:", rtl=True, size=16),
            ft.Container(height=8),
            date_input
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, tight=True)

        actions = [
            ft.TextButton("ביטול", on_click=on_cancel),
            ft.ElevatedButton(
                "עדכן", 
                on_click=on_confirm,
                bgcolor=ft.Colors.DEEP_PURPLE_500,
                color=ft.Colors.WHITE,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
            ),
        ]

        self.show_modern_dialog("ערוך תאריך", content, actions)

    def delete_date_dialog(self, date: str):
        """Show delete confirmation dialog"""
        def confirm_delete(e):
            try:
                if date in self.attendance_data:
                    del self.attendance_data[date]
                    self.save_attendance()
                    self.page.close(dlg)
                    # רענון מלא של הטבלה
                    self.load_data()  # טען מחדש את הנתונים
                    if self.main_content:
                        new_content = self.create_page_content()
                        self.main_content.content = new_content
                        self.main_content.update()
                    self.show_success_snackbar("התאריך נמחק בהצלחה!")
            except Exception as ex:
                print(f"Error in delete_date: {ex}")
                self.show_error_snackbar("שגיאה במחיקת התאריך")

        def cancel_delete(e):
            self.page.close(dlg)

        content = ft.Column([
            ft.Container(
                content=ft.Icon(ft.Icons.WARNING_AMBER_OUTLINED, size=40, color=ft.Colors.AMBER_500),
                bgcolor=ft.Colors.AMBER_50,
                border_radius=20,
                padding=ft.padding.all(16),
            ),
            ft.Container(height=20),
            ft.Text(
                f"האם אתה בטוח שברצונך למחוק את התאריך {date}?",
                rtl=True,
                text_align=ft.TextAlign.CENTER,
                size=14,
                color=ft.Colors.GREY_700
            ),
            ft.Container(height=8),
            ft.Text(
                "פעולה זו לא ניתנת לביטול!",
                rtl=True,
                text_align=ft.TextAlign.CENTER,
                size=12,
                color=ft.Colors.RED_600,
                weight=ft.FontWeight.W_500
            ),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, tight=True)

        actions = [
            ft.TextButton(
                "ביטול", 
                on_click=cancel_delete,
                style=ft.ButtonStyle(color=ft.Colors.GREY_600)
            ),
            ft.ElevatedButton(
                "מחק",
                on_click=confirm_delete,
                bgcolor=ft.Colors.RED_500,
                color=ft.Colors.WHITE,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=8),
                    padding=ft.padding.symmetric(horizontal=24, vertical=12)
                )
            ),
        ]

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("מחיקת תאריך", rtl=True, size=18, weight=ft.FontWeight.W_600, color=ft.Colors.GREY_800),
            content=content,
            actions=actions,
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=16),
        )
        
        self.page.open(dlg)

    def close_dialog(self):
        """Close the current dialog"""
        try:
            # אם יש דיאלוג פתוח, סגור אותו
            if hasattr(self.page, 'dialog') and self.page.dialog:
                self.page.close(self.page.dialog)
        except Exception as e:
            print(f"Error closing dialog: {e}")

    def show_success_snackbar(self, message: str):
        """Show success snackbar"""
        try:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(message, rtl=True, color=ft.Colors.WHITE),
                bgcolor=ft.Colors.GREEN_500,
            )
            self.page.snack_bar.open = True
            self.page.update()
        except Exception as e:
            print(f"Error showing success snackbar: {e}")

    def show_error_snackbar(self, message: str):
        """Show error snackbar"""
        try:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(message, rtl=True, color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_500,
            )
            self.page.snack_bar.open = True
            self.page.update()
        except Exception as e:
            print(f"Error showing error snackbar: {e}")

    def go_back(self, e):
        """Navigate back to attendance page"""
        try:
            if self.navigation_handler:
                # Navigate back to attendance page (index 2)
                self.navigation_handler(None, 2)
        except Exception as ex:
            print(f"Error in go_back: {ex}")

    def go_to_daily_attendance(self, e):
        """Navigate to daily attendance page"""
        try:
            if self.navigation_handler:
                from attendance_table_page import AttendanceTablePage
                # Get today's date
                import datetime
                today = datetime.datetime.now().strftime("%d/%m/%Y")
                daily_page = AttendanceTablePage(self.page, self.navigation_handler, self.group, today)
                self.navigation_handler(daily_page, None)
        except Exception as ex:
            print(f"Error in go_to_daily_attendance: {ex}")
            self.show_error_snackbar("שגיאה במעבר לנוכחות יומית")

    def refresh_page(self):
        """Refresh the entire page"""
        try:
            self.checkboxes.clear()
            if self.main_content:
                # Reload data
                self.load_attendance()
                self.load_students()
                
                # Recreate content
                new_content = self.create_page_content()
                self.main_content.content = new_content
                self.main_content.update()
                
                # Refresh table view if exists
                self.refresh_table_view()
        except Exception as e:
            print(f"Error refreshing page: {e}")

    def create_page_content(self):
        """Create the main page content"""
        try:
            return ft.Column([
                self.create_header_card(),
                self.create_stats_card(),
                self.create_actions_card(),
                self.create_attendance_table_card(),
            ], 
            spacing=24,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            )
        except Exception as e:
            print(f"Error creating page content: {e}")
            # Return error state
            return ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.ERROR, size=64, color=ft.Colors.RED_400),
                    ft.Text("שגיאה בטעינת הדף", rtl=True, size=18, color=ft.Colors.RED_600),
                    ft.Text(str(e), size=14, color=ft.Colors.GREY_600),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.padding.all(40),
                alignment=ft.alignment.center,
            )

    def get_view(self):
        """Get the main view with clean design"""
        try:
            # Create the main content container
            self.main_content = ft.Container(
                content=self.create_page_content(),
                padding=ft.padding.all(24),
                expand=True,
                bgcolor=ft.Colors.GREY_50,  # רקע נקי ואחיד
            )

            # Return simple clean view without gradient
            return self.main_content
            
        except Exception as e:
            print(f"Error creating view: {e}")
            # Return simple error view
            return ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.ERROR_OUTLINE, size=64, color=ft.Colors.RED_400),
                    ft.Text("שגיאה בטעינת העמוד", rtl=True, size=20, color=ft.Colors.RED_600),
                    ft.Text("אנא נסה שוב מאוחר יותר", rtl=True, size=16, color=ft.Colors.GREY_600),
                    ft.Container(height=20),
                    ft.ElevatedButton(
                        "חזרה",
                        on_click=self.go_back,
                        bgcolor=ft.Colors.BLUE_600,
                        color=ft.Colors.WHITE,
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.padding.all(40),
                alignment=ft.alignment.center,
                expand=True,
                bgcolor=ft.Colors.WHITE,
            )

        
    def refresh_table_view(self):
        """Refresh the table view specifically"""
        try:
            if hasattr(self, 'table_view') and self.table_view:
                self.table_view.refresh_table()
        except Exception as e:
            print(f"Error refreshing table view: {e}")
    
    def load_data(self):
        """Load attendance and student data"""
        # Load attendance
        path = f"attendances/attendance_{self.group.get('id', '')}.json"
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self.attendance_data = json.load(f)
            except Exception as e:
                print(f"Error loading attendance: {e}")
                self.attendance_data = {}
        
        # Load students
        try:
            if os.path.exists("data/students.json"):
                with open("data/students.json", "r", encoding="utf-8") as f:
                    students_data = json.load(f)
                    self.students = []
                    for s in students_data.get("students", []):
                        if s.get("group", "").strip() == self.group.get("name", "").strip():
                            self.students.append({"id": s["id"], "name": s["name"]})
        except Exception as e:
            print(f"Error loading students: {e}")

    def refresh_view(self):
        """Refresh the view after data changes"""
        try:
            # Reload data
            self.load_data()
            
            # Recreate the main content
            if self.main_content:
                new_content = self.create_page_content()
                self.main_content.content = new_content
                self.main_content.update()
                
        except Exception as e:
            print(f"Error refreshing view: {e}")
            self.show_error_snackbar("שגיאה ברענון הנתונים")


