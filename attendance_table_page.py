import os
import json
import flet as ft
from typing import Dict, Any, List, Optional

class AttendanceTablePage:
    def __init__(self, page: ft.Page, navigation_handler=None, group: Dict[str, Any] = None, date: str = ""):
        self.page = page
        self.navigation_handler = navigation_handler
        self.group = group or {}
        
        # If no date provided, use today's date
        if not date:
            import datetime
            self.date = datetime.datetime.now().strftime("%d/%m/%Y")
        else:
            self.date = date
            
        self.attendance_data = {}
        self.checkboxes = {}  # Store checkbox references
        
        # Load students for this group
        self.students = self.load_students_for_group()
        
        # Load attendance data
        self.load_attendance()

    def load_students_for_group(self):
        """Load students for the specific group from students.json"""
        try:
            with open("data/students.json", "r", encoding="utf-8") as f:
                students_data = json.load(f)
                group_students = []
                
                for student in students_data.get("students", []):
                    # Check if student belongs to this group
                    if student.get("group", "").strip() == self.group.get("name", "").strip():
                        group_students.append({
                            "id": student.get("id", ""),
                            "name": student.get("name", ""),
                            "group": student.get("group", "")
                        })
                
                return group_students
        except Exception as e:
            print(f"Error loading students: {e}")
            return []

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
        
        # Initialize date if not exists
        if self.date not in self.attendance_data:
            self.attendance_data[self.date] = {}

    def save_attendance(self):
        """Save attendance data to JSON file"""
        try:
            os.makedirs("attendances", exist_ok=True)
            path = f"attendances/attendance_{self.group.get('id', '')}.json"
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.attendance_data, f, ensure_ascii=False, indent=2)
            
            # Show success feedback
            self.show_success_message("הנוכחות נשמרה בהצלחה!")
            
        except Exception as e:
            print(f"Error saving attendance: {e}")
            self.show_error_message("שגיאה בשמירת הנוכחות")

    def create_animated_card(self, content, bgcolor=ft.Colors.WHITE, padding=15):
        """Create an animated card container"""
        return ft.Container(
            content=content,
            bgcolor=bgcolor,
            border_radius=8,
            padding=ft.padding.all(padding),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                offset=ft.Offset(0, 4),
            ),
            animate=ft.Animation(500, ft.AnimationCurve.EASE_OUT),
        )

    def create_header_card(self):
        """Create the header card with title and subtitle"""
        header_content = ft.Column([
            ft.Text(
                "רשימת נוכחות",
                size=24,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_GREY_800,
                text_align=ft.TextAlign.CENTER,
                rtl=True
            ),
            ft.Text(
                f"{self.group.get('name', '')} - {self.date}",
                size=16,
                color=ft.Colors.GREY_600,
                text_align=ft.TextAlign.CENTER,
                rtl=True
            ),
        ], 
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10
        )
        
        return self.create_animated_card(header_content)

    def create_attendance_header(self):
        """Create attendance list header"""
        return ft.Container(
            content=ft.Row([
                ft.Text(
                    "נוכחות",
                    size=12,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "שם התלמידה",
                    size=12,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                    text_align=ft.TextAlign.CENTER,
                    rtl=True,
                    expand=True,
                ),
            ], 
            spacing=10
            ),
            bgcolor=ft.Colors.BLUE_600,
            border_radius=ft.border_radius.only(top_left=6, top_right=6),
            padding=ft.padding.symmetric(horizontal=15, vertical=10),
        )

    def on_checkbox_change(self, student_id: str, e):
        """Handle checkbox state change"""
        is_checked = e.control.value
        self.attendance_data[self.date][str(student_id)] = is_checked

    def create_enhanced_student_card(self, student: Dict[str, Any], present: bool, index: int):
        """Create an enhanced student attendance card with better styling"""
        student_id = str(student.get("id", ""))
        
        # Create custom styled checkbox
        checkbox = ft.Checkbox(
            value=present,
            on_change=lambda e: self.on_checkbox_change(student.get("id", ""), e),
            active_color=ft.Colors.BLUE_600,
            check_color=ft.Colors.WHITE,
            scale=1.2,
        )
        
        # Store checkbox reference
        self.checkboxes[student_id] = checkbox

        def on_hover(e):
            if e.data == "true":
                e.control.bgcolor = ft.Colors.BLUE_50
                e.control.scale = 1.02
            else:
                e.control.bgcolor = ft.Colors.WHITE if index % 2 == 0 else ft.Colors.GREY_50
                e.control.scale = 1.0
            e.control.update()

        # Alternate row colors
        row_color = ft.Colors.WHITE if index % 2 == 0 else ft.Colors.GREY_50

        return ft.Container(
            content=ft.Row([
                checkbox,
                ft.Container(
                    content=ft.Text(
                        student.get("name", ""),
                        size=13,
                        color=ft.Colors.BLUE_GREY_800,
                        rtl=True,
                        weight=ft.FontWeight.W_500,
                    ),
                    expand=True,
                    alignment=ft.alignment.center_right,
                ),
                ft.Container(
                    content=ft.Icon(
                        ft.Icons.PERSON,
                        size=16,
                        color=ft.Colors.BLUE_400,
                    ),
                    width=30,
                    alignment=ft.alignment.center,
                ),
            ], 
            spacing=10
            ),
            bgcolor=row_color,
            padding=ft.padding.symmetric(horizontal=15, vertical=8),
            border_radius=8,
            margin=ft.margin.only(bottom=2),
            on_hover=on_hover,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
            animate_scale=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
        )

    def create_enhanced_attendance_list_card(self):
        """Create enhanced attendance list card with better styling"""
        students = self.students
        
        if not students:
            # Enhanced empty state
            empty_content = ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.PERSON_OFF, size=64, color=ft.Colors.GREY_400),
                    ft.Text(
                        "אין תלמידות בקבוצה זו",
                        size=16,
                        color=ft.Colors.GREY_600,
                        text_align=ft.TextAlign.CENTER,
                        rtl=True
                    ),
                    ft.Text(
                        "הוסף תלמידות לקבוצה כדי לנהל נוכחות",
                        size=14,
                        color=ft.Colors.GREY_500,
                        text_align=ft.TextAlign.CENTER,
                        rtl=True
                    ),
                ], 
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10
                ),
                padding=ft.padding.all(40),
                alignment=ft.alignment.center,
            )
            return self.create_animated_card(empty_content)

        # Create enhanced student cards
        student_cards = []
        for index, student in enumerate(students):
            present = self.attendance_data.get(self.date, {}).get(str(student.get("id", "")), False)
            student_card = self.create_enhanced_student_card(student, present, index)
            student_cards.append(student_card)

        # Statistics section
        total_students = len(students)
        present_count = sum(1 for student in students 
                          if self.attendance_data.get(self.date, {}).get(str(student.get("id", "")), False))
        absent_count = total_students - present_count

        stats_row = ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Column([
                        ft.Text(str(total_students), size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_600),
                        ft.Text("סה״כ", size=12, color=ft.Colors.GREY_600, rtl=True),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                    bgcolor=ft.Colors.BLUE_50,
                    padding=ft.padding.all(8),
                    border_radius=6,
                    expand=True,
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text(str(present_count), size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_600),
                        ft.Text("נוכחות", size=12, color=ft.Colors.GREY_600, rtl=True),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                    bgcolor=ft.Colors.GREEN_50,
                    padding=ft.padding.all(8),
                    border_radius=6,
                    expand=True,
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text(str(absent_count), size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_600),
                        ft.Text("היעדרות", size=12, color=ft.Colors.GREY_600, rtl=True),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                    bgcolor=ft.Colors.RED_50,
                    padding=ft.padding.all(8),
                    border_radius=6,
                    expand=True,
                ),
            ], spacing=8),
            margin=ft.margin.only(bottom=10),
        )

        # Create scrollable list with header
        attendance_content = ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.LIST_ALT, size=20, color=ft.Colors.BLUE_600),
                ft.Text(
                    f"רשימת נוכחות - {self.date}",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_GREY_800,
                    rtl=True
                )
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
            
            ft.Divider(height=1, color=ft.Colors.GREY_300),
            
            stats_row,
            
            self.create_attendance_header(),
            
            ft.Container(
                content=ft.Column(
                    controls=student_cards,
                    spacing=1,
                    scroll=ft.ScrollMode.AUTO,
                ),
                height=350,  # Fixed height for scrolling
                border=ft.border.all(1, ft.Colors.GREY_200),
                border_radius=ft.border_radius.only(bottom_left=6, bottom_right=6),
            )
        ], spacing=10)

        return self.create_animated_card(attendance_content, padding=15)

    def create_quick_actions_card(self):
        """Create quick actions card with bulk operations"""
        def mark_all_present(e):
            for student in self.students:
                student_id = str(student.get("id", ""))
                if student_id in self.checkboxes:
                    self.checkboxes[student_id].value = True
                    self.attendance_data[self.date][student_id] = True
            self.page.update()

        def mark_all_absent(e):
            for student in self.students:
                student_id = str(student.get("id", ""))
                if student_id in self.checkboxes:
                    self.checkboxes[student_id].value = False
                    self.attendance_data[self.date][student_id] = False
            self.page.update()

        quick_actions = ft.Row([
            ft.ElevatedButton(
                text="סמן הכל כנוכח",
                on_click=mark_all_present,
                bgcolor=ft.Colors.GREEN_500,
                color=ft.Colors.WHITE,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=6),
                    padding=ft.padding.symmetric(horizontal=15, vertical=8),
                ),
                height=35,
            ),
            ft.ElevatedButton(
                text="סמן הכל כנעדר",
                on_click=mark_all_absent,
                bgcolor=ft.Colors.RED_500,
                color=ft.Colors.WHITE,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=6),
                    padding=ft.padding.symmetric(horizontal=15, vertical=8),
                ),
                height=35,
            ),
        ], 
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        spacing=10
        )

        quick_actions_content = ft.Column([
            ft.Text(
                "פעולות מהירות",
                size=14,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_GREY_800,
                text_align=ft.TextAlign.CENTER,
                rtl=True
            ),
            quick_actions,
        ], spacing=10)

        return self.create_animated_card(quick_actions_content)

    def show_success_message(self, message: str):
        """Show success message"""
        def close_dialog(e):
            self.page.dialog.open = False
            self.page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("הצלחה", color=ft.Colors.GREEN_600),
            content=ft.Text(message, rtl=True),
            actions=[ft.TextButton("אישור", on_click=close_dialog)],
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def show_error_message(self, message: str):
        """Show error message"""
        def close_dialog(e):
            self.page.dialog.open = False
            self.page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("שגיאה", color=ft.Colors.RED_600),
            content=ft.Text(message, rtl=True),
            actions=[ft.TextButton("אישור", on_click=close_dialog)],
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def save_attendance_with_animation(self, e):
        """Save attendance with visual feedback animation"""
        # Update attendance data from checkboxes
        for student in self.students:
            student_id = str(student.get("id", ""))
            if student_id in self.checkboxes:
                checkbox = self.checkboxes[student_id]
                self.attendance_data[self.date][student_id] = checkbox.value

        # Save to file
        self.save_attendance()

        # Visual feedback - briefly change button color
        save_button = e.control
        original_bgcolor = save_button.bgcolor
        save_button.bgcolor = ft.Colors.GREEN_700
        save_button.update()

    def get_view(self):
        """Get the main view of the attendance table page"""
        # Create all cards
        header_card = self.create_header_card()
        attendance_list_card = self.create_enhanced_attendance_list_card()
        quick_actions_card = self.create_quick_actions_card()
        buttons_card = self.create_enhanced_buttons_card()

        # Main content
        main_content = ft.Container(
            content=ft.Column([
                header_card,
                attendance_list_card,
                quick_actions_card,
                buttons_card,
            ], 
            spacing=20,
            expand=True
            ),
            padding=ft.padding.all(30),
            bgcolor=ft.Colors.GREY_50,
            expand=True,
        )

        return main_content

    def show_date_selection_dialog(self):
        """Show dialog to select new date"""
        date_field = ft.TextField(
            label="תאריך חדש (DD/MM/YYYY)",
            value="",
            rtl=True,
            width=200
        )
        
        def confirm_date(e):
            if date_field.value:
                self.date = date_field.value
                # Initialize new date in attendance data
                if self.date not in self.attendance_data:
                    self.attendance_data[self.date] = {}
                
                # Refresh the view
                self.page.dialog.open = False
                self.page.update()
                
                # Recreate the page with new date
                from attendance_table_page import AttendanceTablePage
                new_page = AttendanceTablePage(self.page, self.navigation_handler, self.group, self.date)
                self.navigation_handler(new_page, None)
        
        def cancel_date(e):
            self.page.dialog.open = False
            self.page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("הוסף תאריך חדש", rtl=True),
            content=ft.Column([
                ft.Text("הכנס תאריך חדש לניהול נוכחות:", rtl=True),
                date_field
            ], tight=True),
            actions=[
                ft.TextButton("ביטול", on_click=cancel_date),
                ft.TextButton("אישור", on_click=confirm_date),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def go_back(self, e):
        """Navigate back"""
        if self.navigation_handler:
            from attendance_page import AttendancePage
            attendance_page = AttendancePage(self.page, self.navigation_handler)
            self.navigation_handler(attendance_page, None)

    def create_enhanced_buttons_card(self):
        """Create enhanced buttons card with better styling"""
        add_date_btn = ft.ElevatedButton(
            text="📅 הוסף תאריך חדש",
            on_click=lambda e: self.show_date_selection_dialog(),
            bgcolor=ft.Colors.ORANGE_600,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=6),
                padding=ft.padding.symmetric(horizontal=20, vertical=12),
            ),
            height=45,
        )

        save_btn = ft.ElevatedButton(
            text="💾 שמור נוכחות",
            on_click=self.save_attendance_with_animation,
            bgcolor=ft.Colors.GREEN_600,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=6),
                padding=ft.padding.symmetric(horizontal=20, vertical=12),
            ),
            height=45,
        )

        back_btn = ft.ElevatedButton(
            text="⬅ חזרה",
            on_click=self.go_back,
            bgcolor=ft.Colors.GREY_600,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=6),
                padding=ft.padding.symmetric(horizontal=20, vertical=12),
            ),
            height=45,
        )

        buttons_content = ft.Row([
            add_date_btn,
            save_btn,
            back_btn,
        ], 
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        spacing=15
        )

        return self.create_animated_card(buttons_content)

class AttendanceCheckBox:
    def __init__(self, date: str, student_id: str, parent_page, is_checked: bool = False):
        self.date = date
        self.student_id = student_id
        self.parent_page = parent_page
        self.is_checked = is_checked
        
    def create_checkbox(self):
        """Create the custom checkbox widget"""
        def on_click(e):
            self.is_checked = not self.is_checked
            self.parent_page.update_attendance(self.date, self.student_id, self.is_checked)
            # Update the checkbox appearance
            e.control.content = self.get_checkbox_content()
            e.control.update()
        
        return ft.Container(
            content=self.get_checkbox_content(),
            width=35,
            height=35,
            border_radius=17.5,  # Make it circular
            on_click=on_click,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
        )
    
    def get_checkbox_content(self):
        """Get the checkbox content based on state"""
        if self.is_checked:
            # Green background with checkmark
            return ft.Container(
                content=ft.Icon(
                    ft.Icons.CHECK,
                    color=ft.Colors.WHITE,
                    size=20,
                ),
                bgcolor=ft.Colors.GREEN_600,
                border=ft.border.all(2, ft.Colors.GREEN_700),
                border_radius=17.5,
                alignment=ft.alignment.center,
            )
        else:
            # Red background with X
            return ft.Container(
                content=ft.Icon(
                    ft.Icons.CLOSE,
                    color=ft.Colors.WHITE,
                    size=20,
                ),
                bgcolor=ft.Colors.RED_600,
                border=ft.border.all(2, ft.Colors.RED_700),
                border_radius=17.5,
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
        self.checkboxes = {}  # Store checkbox references
        
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

    def create_animated_card(self, content, bgcolor=ft.Colors.WHITE, padding=15):
        """Create an animated card container"""
        return ft.Container(
            content=content,
            bgcolor=bgcolor,
            border_radius=8,
            padding=ft.padding.all(padding),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                offset=ft.Offset(0, 4),
            ),
            animate=ft.Animation(500, ft.AnimationCurve.EASE_OUT),
        )

    def create_header_card(self):
        """Create the header card"""
        header_content = ft.Column([
            ft.Text(
                "ניהול נוכחות",
                size=24,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_GREY_800,
                text_align=ft.TextAlign.CENTER,
                rtl=True
            ),
            ft.Text(
                f"קבוצת {self.group.get('name', '')}",
                size=16,
                color=ft.Colors.GREY_600,
                text_align=ft.TextAlign.CENTER,
                rtl=True
            ),
        ], 
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10
        )
        
        return self.create_animated_card(header_content)

    def create_table_header(self):
        """Create table header row"""
        headers = [
            ft.Container(
                content=ft.Text("תאריך", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                bgcolor=ft.Colors.BLUE_600,
                padding=ft.padding.all(10),
                width=120,
                alignment=ft.alignment.center,
            )
        ]
        
        # Add student name headers
        for student in self.students:
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
                    bgcolor=ft.Colors.BLUE_600,
                    padding=ft.padding.all(10),
                    width=100,
                    alignment=ft.alignment.center,
                )
            )
        
        return ft.Row(headers, spacing=1, scroll=ft.ScrollMode.AUTO)

    def create_enhanced_table_row(self, date: str, index: int):
        """Create an enhanced table row with context menu support"""
        row_color = ft.Colors.GREY_50 if index % 2 == 0 else ft.Colors.WHITE
        
        # Date cell with context menu
        def show_date_menu(e):
            self.show_context_menu_dialog(date)

        date_cell = ft.Container(
            content=ft.Text(
                date,
                size=13,
                text_align=ft.TextAlign.CENTER,
                weight=ft.FontWeight.BOLD
            ),
            bgcolor=row_color,
            padding=ft.padding.all(10),
            width=120,
            alignment=ft.alignment.center,
            on_click=show_date_menu,  # Add click handler for context menu
            border=ft.border.all(1, ft.Colors.TRANSPARENT),
            border_radius=4,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
        )

        cells = [date_cell]
        
        # Student attendance cells
        for student in self.students:
            # Get current attendance state
            is_present = False
            if date in self.attendance_data:
                is_present = self.attendance_data[date].get(str(student["id"]), False)
            
            # Create checkbox
            checkbox = AttendanceCheckBox(date, student["id"], self, is_present)
            checkbox_widget = checkbox.create_checkbox()
            
            # Store checkbox reference
            checkbox_key = f"{date}_{student['id']}"
            self.checkboxes[checkbox_key] = checkbox
            
            cells.append(
                ft.Container(
                    content=checkbox_widget,
                    bgcolor=row_color,
                    padding=ft.padding.all(10),
                    width=100,
                    alignment=ft.alignment.center,
                )
            )
        
        return ft.Row(cells, spacing=1, scroll=ft.ScrollMode.AUTO)

    def create_enhanced_attendance_table_card(self):
        """Create enhanced attendance table card with context menu support"""
        dates = list(self.attendance_data.keys())
        
        if not dates and not self.students:
            # Empty state
            empty_content = ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.EVENT_NOTE, size=64, color=ft.Colors.GREY_400),
                    ft.Text(
                        "אין תאריכים או תלמידים להצגה",
                        size=16,
                        color=ft.Colors.GREY_600,
                        text_align=ft.TextAlign.CENTER,
                        rtl=True
                    ),
                    ft.Text(
                        "הוסף תאריך חדש כדי להתחיל",
                        size=14,
                        color=ft.Colors.GREY_500,
                        text_align=ft.TextAlign.CENTER,
                        rtl=True
                    ),
                ], 
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10
                ),
                padding=ft.padding.all(40),
                alignment=ft.alignment.center,
            )
            return self.create_animated_card(empty_content)
        
        # Create table
        table_rows = []
        
        if self.students:  # Only show header if there are students
            table_rows.append(self.create_table_header())
            
            # Add date rows with enhanced functionality
            for index, date in enumerate(dates):
                table_rows.append(self.create_enhanced_table_row(date, index))
        
        # Instructions text
        instructions = ft.Text(
            "לחץ על תאריך כדי לערוך או למחוק אותו",
            size=12,
            color=ft.Colors.GREY_500,
            text_align=ft.TextAlign.CENTER,
            rtl=True,
            italic=True
        )

        table_content = ft.Column([
            ft.Text(
                "טבלת נוכחות",
                size=14,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_GREY_800,
                rtl=True
            ),
            instructions,
            ft.Container(
                content=ft.Column(
                    controls=table_rows,
                    spacing=1,
                    scroll=ft.ScrollMode.AUTO,
                ),
                border=ft.border.all(1, ft.Colors.GREY_300),
                border_radius=6,
                height=400,
            )
        ], spacing=10)

        return self.create_animated_card(table_content, padding=15)

    def show_date_input_dialog(self, title: str, current_date: str = "DD/MM/YYYY", callback=None):
        """Show date input dialog"""
        date_input = ft.TextField(
            value=current_date,
            hint_text="DD/MM/YYYY",
            width=200,
            text_align=ft.TextAlign.CENTER,
        )

        def on_confirm(e):
            if callback and date_input.value:
                callback(date_input.value)
            self.page.dialog.open = False
            self.page.update()

        def on_cancel(e):
            self.page.dialog.open = False
            self.page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(title, rtl=True),
            content=ft.Container(
                content=date_input,
                padding=ft.padding.all(10),
            ),
            actions=[
                ft.TextButton("ביטול", on_click=on_cancel),
                ft.TextButton("אישור", on_click=on_confirm),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def add_new_date(self, e):
        """Add new date"""
        def on_date_added(date: str):
            if date and date not in self.attendance_data:
                # Initialize new date with all students as False (absent)
                self.attendance_data[date] = {}
                for student in self.students:
                    self.attendance_data[date][str(student["id"])] = False
                
                self.save_attendance()
                self.refresh_table()
                self.show_success_message(f"התאריך {date} נוסף בהצלחה!")
            elif date in self.attendance_data:
                self.show_error_message("התאריך הזה כבר קיים!")

        self.show_date_input_dialog("הוסף תאריך", callback=on_date_added)

    def refresh_table(self):
        """Refresh the attendance table"""
        # Recreate the table card
        new_table_card = self.create_enhanced_attendance_table_card()
        
        # Find and replace the table card in the main content
        # This is a simplified approach - in a real app you might want to handle this more elegantly
        self.page.update()

    def show_success_message(self, message: str):
        """Show success message"""
        def close_dialog(e):
            self.page.dialog.open = False
            self.page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("הצלחה", color=ft.Colors.GREEN_600),
            content=ft.Text(message, rtl=True),
            actions=[ft.TextButton("אישור", on_click=close_dialog)],
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def show_error_message(self, message: str):
        """Show error message"""
        def close_dialog(e):
            self.page.dialog.open = False
            self.page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("שגיאה", color=ft.Colors.RED_600),
            content=ft.Text(message, rtl=True),
            actions=[ft.TextButton("אישור", on_click=close_dialog)],
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def show_context_menu_dialog(self, date: str):
        """Show context menu options for a date"""
        def edit_date(e):
            self.page.dialog.open = False
            self.page.update()
            self.edit_date_dialog(date)

        def delete_date(e):
            self.page.dialog.open = False
            self.page.update()
            self.delete_date_dialog(date)

        def close_menu(e):
            self.page.dialog.open = False
            self.page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"פעולות עבור {date}", rtl=True),
            content=ft.Column([
                ft.TextButton(
                    text="ערוך תאריך",
                    on_click=edit_date,
                    style=ft.ButtonStyle(
                        color=ft.Colors.BLUE_600,
                    )
                ),
                ft.TextButton(
                    text="מחק תאריך",
                    on_click=delete_date,
                    style=ft.ButtonStyle(
                        color=ft.Colors.RED_600,
                    )
                ),
            ], tight=True),
            actions=[
                ft.TextButton("ביטול", on_click=close_menu),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def edit_date_dialog(self, current_date: str):
        """Show edit date dialog"""
        def on_date_edited(new_date: str):
            if new_date and new_date != current_date:
                if new_date not in self.attendance_data:
                    # Update attendance data
                    self.attendance_data[new_date] = self.attendance_data.pop(current_date)
                    self.save_attendance()
                    self.refresh_table()
                    self.show_success_message(f"התאריך עודכן ל-{new_date}")
                else:
                    self.show_error_message("התאריך הזה כבר קיים!")

        self.show_date_input_dialog("ערוך תאריך", current_date, on_date_edited)

    def delete_date_dialog(self, date: str):
        """Show delete confirmation dialog"""
        def confirm_delete(e):
            del self.attendance_data[date]
            self.save_attendance()
            self.refresh_table()
            self.page.dialog.open = False
            self.page.update()
            self.show_success_message("התאריך נמחק בהצלחה!")

        def cancel_delete(e):
            self.page.dialog.open = False
            self.page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("מחיקת תאריך", color=ft.Colors.RED_600),
            content=ft.Text(
                f"האם אתה בטוח שברצונך למחוק את התאריך {date}?",
                rtl=True
            ),
            actions=[
                ft.TextButton("ביטול", on_click=cancel_delete),
                ft.TextButton(
                    "מחק", 
                    on_click=confirm_delete,
                    style=ft.ButtonStyle(color=ft.Colors.RED_600)
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def go_back(self, e):
        """Navigate back to groups page"""
        if self.navigation_handler:
            from attendance_page import AttendancePage
            attendance_page = AttendancePage(self.page, self.navigation_handler)
            self.navigation_handler(attendance_page, None)

    def create_actions_card(self):
        """Create the actions card with buttons"""
        add_date_btn = ft.ElevatedButton(
            text="📅 הוסף תאריך חדש",
            on_click=self.add_new_date,
            bgcolor=ft.Colors.BLUE_600,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=6),
                padding=ft.padding.symmetric(horizontal=20, vertical=12),
            ),
            height=40,
        )

        back_btn = ft.ElevatedButton(
            text="⬅ חזרה לקבוצות",
            on_click=self.go_back,
            bgcolor=ft.Colors.RED_600,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=6),
                padding=ft.padding.symmetric(horizontal=20, vertical=12),
            ),
            height=40,
        )

        actions_content = ft.Row([
            add_date_btn,
            back_btn,
        ], 
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        spacing=10
        )

        return self.create_animated_card(actions_content)

    def get_view(self):
        """Get the main view of the group attendance page"""
        # Create all cards
        header_card = self.create_header_card()
        table_card = self.create_enhanced_attendance_table_card()
        actions_card = self.create_actions_card()

        # Main content
        main_content = ft.Container(
            content=ft.Column([
                header_card,
                table_card,
                actions_card,
            ], 
            spacing=20,
            expand=True
            ),
            padding=ft.padding.all(30),
            bgcolor=ft.Colors.GREY_50,
            expand=True,
        )

        return main_content
