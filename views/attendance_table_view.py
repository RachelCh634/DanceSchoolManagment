"""
Represents a view for displaying and managing attendance data for a specific group.

This class provides a comprehensive interface for tracking student attendance, 
including features like:
- Loading and saving attendance data
- Creating an interactive attendance table
- Editing and deleting attendance records
- Displaying attendance statistics

Attributes:
    page (ft.Page): The Flet page context for rendering UI
    group (Dict[str, Any]): Group information for which attendance is being tracked
    attendance_data (Dict): Dictionary storing attendance records
    students (List[Dict]): List of students in the group
"""
import json
import os
import flet as ft
from typing import Dict, Any
from utils.attendance_utils import AttendanceUtils

class AttendanceTableView:
    def __init__(self, page: ft.Page, navigation_handler=None, group: Dict[str, Any] = None, parent_page=None):
        self.page = page
        self.navigation_handler = navigation_handler
        self.group = group or {}
        self.parent_page = parent_page  
        self.attendance_data = {}
        self.students = []
        self.main_content = None
        
        # Load data
        self.load_data()

    def load_data(self):
        """Load attendance and student data"""
        # ✅ Load attendance using utility
        self.attendance_data = AttendanceUtils.load_attendance_file(self.group.get('id', ''))
        
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

    def save_attendance(self):
        """Save attendance data - ✅ SILENT VERSION"""
        try:
            AttendanceUtils.save_attendance_file(self.group.get('id', ''), self.attendance_data)
            # ✅ ללא refresh - רק שמירה
        except Exception as e:
            print(f"Error saving attendance: {e}")

    def create_modern_data_table(self):
        """Create modern React-style table with clean design and horizontal scroll"""
        dates = list(self.attendance_data.keys())
        
        if not dates or not self.students:
            return self.create_empty_table_state()
        
        # Create table header
        header_row = self.create_table_header()
        
        # Create table rows
        table_rows = []
        for date in sorted(dates, reverse=True):
            table_rows.append(self.create_table_row(date))
        
        # Create the table content with horizontal scroll
        table_content = ft.Column([
            header_row,
            ft.Container(height=1, bgcolor=ft.Colors.GREY_200),  # Header separator
            ft.Column(table_rows, spacing=0),
        ], spacing=0)
        
        # Wrap table in horizontal scroll container
        scrollable_table = ft.Container(
            content=ft.Row([
                table_content
            ], scroll=ft.ScrollMode.AUTO),  # Enable horizontal scroll
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
            # Set minimum width to force horizontal scroll when needed
            width=None,  # Let it expand naturally
            height=None,  # Let it expand naturally
        )
        
        return scrollable_table

    def create_table_header(self):
        """Create React-style table header with fixed widths"""
        header_cells = [
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.CALENDAR_TODAY, size=16, color=ft.Colors.GREY_600),
                    ft.Container(width=8),
                    ft.Text(
                        "תאריך", 
                        size=14, 
                        weight=ft.FontWeight.W_600, 
                        color=ft.Colors.GREY_700,
                        rtl=True
                    ),
                ], alignment=ft.MainAxisAlignment.START),
                width=160,  # Increased width for date column
                padding=ft.padding.symmetric(horizontal=16, vertical=16),
            )
        ]
        
        # Add student header cells with fixed widths
        for student in self.students:
            header_cells.append(
                ft.Container(
                    content=ft.Text(
                        student["name"],
                        size=14,
                        weight=ft.FontWeight.W_600,
                        color=ft.Colors.GREY_700,
                        text_align=ft.TextAlign.CENTER,
                        rtl=True,
                        overflow=ft.TextOverflow.ELLIPSIS,  # Handle long names
                    ),
                    width=140,  # Fixed width for each student column
                    padding=ft.padding.symmetric(horizontal=12, vertical=16),
                    alignment=ft.alignment.center,
                    tooltip=student["name"],  # Show full name on hover
                )
            )
        
        return ft.Container(
            content=ft.Row(header_cells, spacing=0),
            bgcolor=ft.Colors.GREY_50,
            border_radius=ft.border_radius.only(top_left=16, top_right=16),
        )

    def create_table_row(self, date: str):
        """Create React-style table row with fixed widths"""
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
                width=160,  # Fixed width matching header
                padding=ft.padding.symmetric(horizontal=16, vertical=12),
                on_click=lambda e, d=date: self.show_date_options(d),
                ink=True,
                border_radius=8,
                tooltip="לחץ לעריכה",
            )
        ]
        
        # Add attendance cells with fixed widths
        for student in self.students:
            is_present = self.attendance_data.get(date, {}).get(str(student["id"]), False)
            row_cells.append(
                ft.Container(
                    content=self.create_status_toggle(is_present, date, student["id"]),
                    width=140,  # Fixed width matching header
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

    def on_row_hover(self, e):
        """Handle row hover effect"""
        if e.data == "true":
            e.control.bgcolor = ft.Colors.GREY_50
        else:
            e.control.bgcolor = ft.Colors.WHITE
        e.control.update()

    def create_status_toggle(self, is_present: bool, date: str, student_id: str):
        """Create clean icon-only status toggle button"""
        def toggle_attendance(e):
            # קבלת הסטטוס הנוכחי מהנתונים
            current_status = self.attendance_data.get(date, {}).get(str(student_id), False)
            new_status = not current_status
            
            if date not in self.attendance_data:
                self.attendance_data[date] = {}
            self.attendance_data[date][str(student_id)] = new_status
            self.save_attendance()
            
            # עדכון מיידי של הכפתור - יצירת אייקון חדש
            if new_status:
                new_icon = ft.Icon(ft.Icons.CHECK_CIRCLE, size=22, color=ft.Colors.GREEN_600)
                e.control.tooltip = "נוכח - לחץ לשינוי"
            else:
                new_icon = ft.Icon(ft.Icons.CLOSE, size=22, color=ft.Colors.RED_500)
                e.control.tooltip = "נעדר - לחץ לשינוי"
            
            # החלפת התוכן
            e.control.content = new_icon
            e.control.update()
            
            self.show_success_snackbar(f"נוכחות עודכנה ל{'נוכח' if new_status else 'נעדר'}")
        
        # קבלת הסטטוס הנוכחי מהנתונים
        current_status = self.attendance_data.get(date, {}).get(str(student_id), False)
        
        # יצירת האייקון הנכון
        if current_status:
            icon = ft.Icon(ft.Icons.CHECK_CIRCLE, size=22, color=ft.Colors.GREEN_600)
            tooltip_text = "נוכח - לחץ לשינוי"
        else:
            icon = ft.Icon(ft.Icons.CLOSE, size=22, color=ft.Colors.RED_500)
            tooltip_text = "נעדר - לחץ לשינוי"
        
        return ft.Container(
            content=icon,
            padding=ft.padding.all(8),
            border_radius=8,
            on_click=toggle_attendance,
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
            tooltip=tooltip_text,
            ink=True,
            width=40,
            height=40,
            alignment=ft.alignment.center,
        )


    def create_empty_table_state(self):
        """Create empty state for table"""
        return ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.TABLE_VIEW_OUTLINED, size=64, color=ft.Colors.GREY_300),
                ft.Container(height=20),
                ft.Text(
                    "אין נתונים להצגה",
                    size=18,
                    weight=ft.FontWeight.W_600,
                    color=ft.Colors.GREY_600,
                    text_align=ft.TextAlign.CENTER,
                    rtl=True
                ),
                ft.Container(height=8),
                ft.Text(
                    "הוסף תאריכים ותלמידים כדי לראות את הטבלה",
                    size=14,
                    color=ft.Colors.GREY_500,
                    text_align=ft.TextAlign.CENTER,
                    rtl=True
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.all(80),
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.WHITE,
            border_radius=16,
            border=ft.border.all(1, ft.Colors.GREY_200),
        )

    def create_header_section(self):
        """Create header section with navigation and title"""
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.IconButton(
                        ft.Icons.ARROW_BACK_IOS,
                        on_click=self.go_back,
                        icon_color=ft.Colors.GREY_600,
                        icon_size=20,
                        tooltip="חזרה לעמוד הקבוצה",
                    ),
                    bgcolor=ft.Colors.GREY_100,
                    border_radius=12,
                    padding=ft.padding.all(4),
                ),
                ft.Container(width=16),
                ft.Column([
                    ft.Text(
                        "טבלת נוכחות מלאה",
                        size=24,
                        weight=ft.FontWeight.W_700,
                        color=ft.Colors.GREY_800,
                        rtl=True,
                    ),
                    ft.Text(
                        f"קבוצת {self.group.get('name', '')}",
                        size=14,
                        color=ft.Colors.GREY_500,
                        rtl=True,
                    ),
                ], spacing=4),
                ft.Container(expand=True),
                ft.Row([
                    ft.Container(
                        content=ft.IconButton(
                            ft.Icons.REFRESH_OUTLINED,
                            on_click=self.refresh_table,
                            icon_color=ft.Colors.GREY_600,
                            icon_size=20,
                            tooltip="רענן נתונים",
                        ),
                        bgcolor=ft.Colors.GREY_100,
                        border_radius=12,
                        padding=ft.padding.all(4),
                    ),
                    ft.Container(width=8),
                ]),
            ]),
            padding=ft.padding.all(24),
            bgcolor=ft.Colors.WHITE,
            border_radius=16,
            border=ft.border.all(1, ft.Colors.GREY_200),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=20,
                color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                offset=ft.Offset(0, 4),
            ),
        )

    def show_date_options(self, date: str):
        """Show options for date (edit/delete)"""
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
                content=ft.ListTile(
                    leading=ft.Icon(ft.Icons.EDIT_OUTLINED, color=ft.Colors.BLUE_500, size=20),
                    title=ft.Text("ערוך תאריך", rtl=True, size=14, color=ft.Colors.GREY_700),
                    on_click=edit_date,
                ),
                border_radius=8,
                ink=True,
            ),
            ft.Container(height=4),
            ft.Container(
                content=ft.ListTile(
                    leading=ft.Icon(ft.Icons.DELETE_OUTLINE, color=ft.Colors.RED_500, size=20),
                    title=ft.Text("מחק תאריך", rtl=True, size=14, color=ft.Colors.GREY_700),
                    on_click=delete_date,
                ),
                border_radius=8,
                ink=True,
            ),
        ], tight=True, spacing=0)

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"פעולות עבור {date}", rtl=True, size=16, weight=ft.FontWeight.W_600, color=ft.Colors.GREY_800),
            content=content,
            actions=[
                ft.TextButton(
                    "ביטול", 
                    on_click=close_menu,
                    style=ft.ButtonStyle(color=ft.Colors.GREY_600)
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=16),
        )
        
        self.page.open(dlg)

    def edit_date_dialog(self, current_date: str):
        """Show edit date dialog"""
        date_input = ft.TextField(
            value=current_date,
            width=280,
            text_align=ft.TextAlign.CENTER,
            border_radius=12,
            bgcolor=ft.Colors.GREY_50,
            border_color=ft.Colors.GREY_200,
            focused_border_color=ft.Colors.BLUE_400,
            text_size=14,
            autofocus=True,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
        )

        def on_confirm(e):
            try:
                new_date = date_input.value.strip() if date_input.value else ""
                
                # ✅ Validate new date
                if not AttendanceUtils.validate_date(new_date):
                    self.show_error_snackbar("אנא הכנס תאריך תקין!")
                    return
                
                if new_date != current_date:
                    if new_date not in self.attendance_data:
                        # Move data from old date to new date
                        self.attendance_data[new_date] = self.attendance_data.pop(current_date)
                        self.save_attendance()
                        self.page.close(dlg)
                        
                        # ✅ Trigger parent refresh
                        if self.parent_page and hasattr(self.parent_page, 'refresh_view'):
                            self.parent_page.refresh_view()
                        
                        self.show_success_snackbar(f"התאריך עודכן ל-{new_date}")
                    else:
                        self.show_error_snackbar("התאריך הזה כבר קיים!")
                else:
                    self.page.close(dlg)
                    
            except Exception as ex:
                print(f"Error in edit_date: {ex}")
                self.show_error_snackbar("שגיאה בעריכת התאריך")

        def on_cancel(e):
            self.page.close(dlg)

        content = ft.Column([
            ft.Container(
                content=ft.Icon(ft.Icons.EDIT_CALENDAR_OUTLINED, size=40, color=ft.Colors.BLUE_500),
                bgcolor=ft.Colors.BLUE_50,
                border_radius=20,
                padding=ft.padding.all(16),
            ),
            ft.Container(height=20),
            ft.Text("ערוך את התאריך:", rtl=True, size=14, color=ft.Colors.GREY_700),
            ft.Container(height=12),
            date_input
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, tight=True)

        actions = [
            ft.TextButton(
                "ביטול", 
                on_click=on_cancel,
                style=ft.ButtonStyle(color=ft.Colors.GREY_600)
            ),
            ft.ElevatedButton(
                "עדכן", 
                on_click=on_confirm,
                bgcolor=ft.Colors.BLUE_500,
                color=ft.Colors.WHITE,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=8),
                    padding=ft.padding.symmetric(horizontal=24, vertical=12)
                )
            ),
        ]

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("ערוך תאריך", rtl=True, size=18, weight=ft.FontWeight.W_600, color=ft.Colors.GREY_800),
            content=content,
            actions=actions,
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=16),
        )
        
        self.page.open(dlg)

    def delete_date_dialog(self, date: str):
        """Show delete confirmation dialog"""
        def confirm_delete(e):
            try:
                if date in self.attendance_data:
                    del self.attendance_data[date]
                    self.save_attendance()
                    self.page.close(dlg)
                    
                    # ✅ Trigger parent refresh
                    if self.parent_page and hasattr(self.parent_page, 'refresh_view'):
                        self.parent_page.refresh_view()
                    
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

    def show_success_snackbar(self, message: str):
        """Show success snackbar"""
        try:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Row([
                    ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, color=ft.Colors.WHITE, size=20),
                    ft.Container(width=8),
                    ft.Text(message, rtl=True, color=ft.Colors.WHITE, size=14),
                ]),
                bgcolor=ft.Colors.GREEN_500,
                shape=ft.RoundedRectangleBorder(radius=12),
            )
            self.page.snack_bar.open = True
            self.page.update()
        except Exception as e:
            print(f"Error showing success snackbar: {e}")

    def show_error_snackbar(self, message: str):
        """Show error snackbar"""
        try:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Row([
                    ft.Icon(ft.Icons.ERROR_OUTLINE, color=ft.Colors.WHITE, size=20),
                    ft.Container(width=8),
                    ft.Text(message, rtl=True, color=ft.Colors.WHITE, size=14),
                ]),
                bgcolor=ft.Colors.RED_500,
                shape=ft.RoundedRectangleBorder(radius=12),
            )
            self.page.snack_bar.open = True
            self.page.update()
        except Exception as e:
            print(f"Error showing error snackbar: {e}")

    # ✅ הוסף את הפונקציה החדשה
    def get_table_only(self):
        """Get only the table component - for embedding in other pages"""
        return self.create_modern_data_table()

    
    def create_stats_section(self):
        """Create statistics section with modern cards"""
        dates = list(self.attendance_data.keys())
        total_classes = len(dates)
        total_students = len(self.students)
        
        if total_classes == 0 or total_students == 0:
            return ft.Container()
        
        # Calculate overall attendance
        total_possible = total_classes * total_students
        total_present = 0
        
        for date in dates:
            for student in self.students:
                if self.attendance_data[date].get(str(student["id"]), False):
                    total_present += 1
        
        attendance_rate = (total_present / total_possible * 100) if total_possible > 0 else 0
        
        return ft.Container(
            content=ft.Row([
                self.create_stat_card("שיעורים", str(total_classes), ft.Icons.CALENDAR_TODAY_OUTLINED, ft.Colors.BLUE_500),
                self.create_stat_card("תלמידים", str(total_students), ft.Icons.PEOPLE_OUTLINE, ft.Colors.PURPLE_500),
                self.create_stat_card("אחוז נוכחות", f"{attendance_rate:.1f}%", ft.Icons.ANALYTICS_OUTLINED, 
                                    ft.Colors.GREEN_500 if attendance_rate >= 80 else ft.Colors.AMBER_500 if attendance_rate >= 60 else ft.Colors.RED_500),
                self.create_stat_card("סה\"כ נוכחויות", str(total_present), ft.Icons.CHECK_CIRCLE_OUTLINE, ft.Colors.TEAL_500),
            ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
            padding=ft.padding.all(20),
        )

    def create_stat_card(self, title: str, value: str, icon, color):
        """Create individual stat card with modern design"""
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Icon(icon, size=24, color=color),
                    bgcolor=ft.Colors.with_opacity(0.1, color),
                    border_radius=12,
                    padding=ft.padding.all(12),
                ),
                ft.Container(height=12),
                ft.Text(value, size=20, weight=ft.FontWeight.W_700, color=ft.Colors.GREY_800),
                ft.Text(title, size=12, color=ft.Colors.GREY_500, rtl=True),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, ft.Colors.GREY_200),
            padding=ft.padding.all(20),
            border_radius=16,
            width=160,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=20,
                color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                offset=ft.Offset(0, 4),
            ),
        )

    def refresh_table(self):
        """Refresh the table data and view"""
        try:
            # Reload data
            self.load_data()
            
            # Recreate the main content
            if self.main_content:
                new_content = self.create_page_content()
                self.main_content.content = new_content
                self.main_content.update()
            
        except Exception as e:
            print(f"Error refreshing table: {e}")
            self.show_error_snackbar("שגיאה ברענון הטבלה")

    def go_back(self, e):
        """Go back to group attendance page"""
        from pages.group_attendance_page import GroupAttendancePage
        try:
            if self.navigation_handler:
                group_page = GroupAttendancePage(self.page, self.navigation_handler, self.group)
                self.navigation_handler(group_page, None)
        except Exception as ex:
            print(f"Error in go_back: {ex}")

    def create_gradient_background(self):
        """Create subtle gradient background"""
        return ft
    
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
        
        # ✅ יצירת הטבלה החדשה עם parent_page
        self.table_view = AttendanceTableView(
            page=self.page, 
            navigation_handler=self.navigation_handler, 
            group=self.group,
            parent_page=self  # ✅ העבר את עצמך כ-parent
        )
        
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

        table_content = ft.Column([
            table_header,
            ft.Container(
                content=self.table_view.get_table_only(),
                expand=True,
            )
        ], spacing=0, tight=True)

        return self.create_modern_card(table_content)

