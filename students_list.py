import json
import os
import flet as ft
from typing import List, Dict, Any

class StudentsListPage:
    def __init__(self, page: ft.Page, navigation_handler=None):
        self.page = page
        self.navigation_handler = navigation_handler
        self.all_students = self.load_students()
        self.filtered_students = self.all_students.copy()
        
        self.search_input = None
        self.students_table = None
        self.no_results_dialog = None
        self.stats_row = None
        
    def load_students(self) -> List[Dict[str, Any]]:
        """Load students data from JSON file"""
        try:
            base_dir = os.path.dirname(__file__)
            json_path = os.path.abspath(os.path.join(base_dir, 'data', 'students.json'))
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("students", [])
        except Exception as e:
            print(f"שגיאה בטעינת students.json: {e}")
            return []

    def filter_students(self, e):
        """Filter students based on search query"""
        query = e.control.value.lower() if e.control.value else ""
        
        if not query:
            self.filtered_students = self.all_students.copy()
        else:
            self.filtered_students = [
                student for student in self.all_students
                if query in json.dumps(student, ensure_ascii=False).lower()
            ]
        
        self.update_table()
        self.update_stats()

    def create_stats_card(self, title, value, icon, color):
        """Create a statistics card"""
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(icon, size=24, color=color),
                    ft.Text(value, size=28, weight=ft.FontWeight.BOLD, color=color)
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                ft.Text(title, size=12, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER, rtl=True)
            ], spacing=8, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=160,
            height=100,
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            padding=ft.padding.all(16),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                offset=ft.Offset(0, 2)
            ),
            border=ft.border.all(1, ft.Colors.with_opacity(0.1, ft.Colors.GREY_400))
        )

    def update_stats(self):
        """Update statistics cards"""
        if not self.stats_row:
            return
            
        total_students = len(self.filtered_students)
        paid_students = len([s for s in self.filtered_students if s.get("payment_status") == "שולם"])
        unpaid_students = total_students - paid_students
        
        self.stats_row.controls = [
            self.create_stats_card("סה״כ תלמידות", str(total_students), ft.Icons.PEOPLE, ft.Colors.BLUE_600),
            self.create_stats_card("שילמו", str(paid_students), ft.Icons.CHECK_CIRCLE, ft.Colors.GREEN_600),
            self.create_stats_card("לא שילמו", str(unpaid_students), ft.Icons.PENDING, ft.Colors.ORANGE_600),
        ]
        self.page.update()

    def create_table_header(self):
        """Create modern table header row"""
        header_style = {
            "bgcolor": ft.Colors.with_opacity(0.8, ft.Colors.BLUE_GREY_900),
            "padding": ft.padding.symmetric(horizontal=16, vertical=20),
            "alignment": ft.alignment.center,
        }
        
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Text("שם התלמידה", size=14, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE),
                    expand=2, **header_style
                ),
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.BADGE, size=16, color=ft.Colors.WHITE70),
                        ft.Text("ת.ז", size=14, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE)
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=4),
                    expand=2, **header_style
                ),
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.PHONE, size=16, color=ft.Colors.WHITE70),
                        ft.Text("טלפון", size=14, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE)
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=4),
                    expand=2, **header_style
                ),
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.GROUP, size=16, color=ft.Colors.WHITE70),
                        ft.Text("קבוצה", size=14, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE)
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=4),
                    expand=2, **header_style
                ),
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.PAYMENT, size=16, color=ft.Colors.WHITE70),
                        ft.Text("סטטוס תשלום", size=14, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE)
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=4),
                    expand=2, **header_style
                ),
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.DATE_RANGE, size=16, color=ft.Colors.WHITE70),
                        ft.Text("תאריך הצטרפות", size=14, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE)
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=4),
                    expand=2, **header_style
                ),
            ], spacing=0),
            border_radius=ft.border_radius.only(top_left=12, top_right=12),
        )

    def create_table_row(self, student: Dict[str, Any], index: int):
        """Create a modern table row for a student"""
        row_color = ft.Colors.with_opacity(0.3, ft.Colors.BLUE_GREY_50) if index % 2 == 0 else ft.Colors.WHITE
        
        # Payment status styling
        payment_status = student.get("payment_status", "")
        if payment_status == "שולם":
            payment_color = ft.Colors.GREEN_600
            payment_bg = ft.Colors.with_opacity(0.1, ft.Colors.GREEN_600)
            payment_icon = ft.Icons.CHECK_CIRCLE
        elif payment_status == "לא שולם" or payment_status == "ממתין":
            payment_color = ft.Colors.ORANGE_600
            payment_bg = ft.Colors.with_opacity(0.1, ft.Colors.ORANGE_600)
            payment_icon = ft.Icons.PENDING
        else:
            payment_color = ft.Colors.GREY_600
            payment_bg = ft.Colors.with_opacity(0.1, ft.Colors.GREY_600)
            payment_icon = ft.Icons.HELP

        cell_style = {
            "bgcolor": row_color,
            "padding": ft.padding.symmetric(horizontal=16, vertical=16),
            "alignment": ft.alignment.center,
        }

        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Text(
                        student.get("name", ""), 
                        size=14, 
                        weight=ft.FontWeight.W_500,
                        text_align=ft.TextAlign.CENTER,
                        rtl=True,
                        color=ft.Colors.BLUE_GREY_800
                    ),
                    expand=2, **cell_style
                ),
                ft.Container(
                    content=ft.Text(
                        student.get("id", ""), 
                        size=13, 
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLUE_GREY_700,
                        font_family="monospace"
                    ),
                    expand=2, **cell_style
                ),
                ft.Container(
                    content=ft.Text(
                        student.get("phone", ""), 
                        size=13, 
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLUE_GREY_700,
                        font_family="monospace"
                    ),
                    expand=2, **cell_style
                ),
                ft.Container(
                    content=ft.Container(
                        content=ft.Text(
                            student.get("group", ""), 
                            size=13, 
                            weight=ft.FontWeight.W_500,
                            text_align=ft.TextAlign.CENTER,
                            rtl=True,
                            color=ft.Colors.BLUE_600
                        ),
                        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLUE_600),
                        padding=ft.padding.symmetric(horizontal=12, vertical=6),
                        border_radius=16,
                    ),
                    expand=2, **cell_style
                ),
                ft.Container(
                    content=ft.Container(
                        content=ft.Row([
                            ft.Icon(payment_icon, size=16, color=payment_color),
                            ft.Text(
                                payment_status, 
                                size=13, 
                                weight=ft.FontWeight.W_500,
                                color=payment_color,
                                rtl=True
                            )
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=4),
                        bgcolor=payment_bg,
                        padding=ft.padding.symmetric(horizontal=12, vertical=6),
                        border_radius=16,
                    ),
                    expand=2, **cell_style
                ),
                ft.Container(
                    content=ft.Text(
                        student.get("join_date", ""), 
                        size=13, 
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLUE_GREY_700
                    ),
                    expand=2, **cell_style
                ),
            ], spacing=0),
            border=ft.border.only(bottom=ft.BorderSide(1, ft.Colors.with_opacity(0.1, ft.Colors.GREY_400))),
        )

    def update_table(self):
        """Update the table with filtered students"""
        if not self.students_table:
            return
        
        table_rows = [self.create_table_header()]
        
        if not self.filtered_students:
            self.show_no_results_dialog()
        else:
            for index, student in enumerate(self.filtered_students):
                table_rows.append(self.create_table_row(student, index))
        
        self.students_table.controls = table_rows
        self.page.update()

    def show_no_results_dialog(self):
        """Show modern dialog when no search results found"""
        def close_dialog(e):
            self.no_results_dialog.open = False
            self.page.update()

        self.no_results_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(ft.Icons.SEARCH_OFF, size=24, color=ft.Colors.ORANGE_600),
                ft.Text("אין תוצאות", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_800)
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
            content=ft.Container(
                content=ft.Column([
                    ft.Text(
                        "לא נמצאה אף תלמידה התואמת לדרישות החיפוש",
                        size=16,
                        color=ft.Colors.BLUE_GREY_600,
                        text_align=ft.TextAlign.CENTER,
                        rtl=True
                    ),
                    ft.Text(
                        "נסה לחפש במילים אחרות או לנקות את שדה החיפוש",
                        size=14,
                        color=ft.Colors.GREY_500,
                        text_align=ft.TextAlign.CENTER,
                        rtl=True
                    )
                ], spacing=8, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.padding.all(16)
            ),
            actions=[
                ft.Container(
                    content=ft.TextButton(
                        "אישור", 
                        on_click=close_dialog,
                        style=ft.ButtonStyle(
                            color=ft.Colors.WHITE,
                            bgcolor=ft.Colors.BLUE_600,
                            shape=ft.RoundedRectangleBorder(radius=8),
                            padding=ft.padding.symmetric(horizontal=24, vertical=12)
                        )
                    ),
                    alignment=ft.alignment.center
                )
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
            shape=ft.RoundedRectangleBorder(radius=16),
        )
        
        self.page.dialog = self.no_results_dialog
        self.no_results_dialog.open = True
        self.page.update()

    def get_view(self):
        """Get the modern main view of the students list page"""
        # Modern title with gradient effect
        title_container = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.SCHOOL, size=32, color=ft.Colors.BLUE_600),
                    ft.Text(
                        "רשימת התלמידות",
                        size=32,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE_GREY_800,
                        rtl=True
                    )
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=12),
                ft.Text(
                    "ניהול ומעקב אחר כל התלמידות במערכת",
                    size=16,
                    color=ft.Colors.BLUE_GREY_500,
                    text_align=ft.TextAlign.CENTER,
                    rtl=True
                )
            ], spacing=8, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.only(bottom=32),
            alignment=ft.alignment.center
        )

        # Modern search input
        self.search_input = ft.TextField(
            hint_text="חיפוש לפי שם, קבוצה, טלפון או כל פרט אחר...",
            hint_style=ft.TextStyle(color=ft.Colors.GREY_500),
            text_size=14,
            height=50,
            border_color=ft.Colors.BLUE_400,
            border_width=2,
            border_radius=12,
            filled=True,
            fill_color=ft.Colors.WHITE,
            on_change=self.filter_students,
            rtl=True,
            text_align=ft.TextAlign.RIGHT,
            prefix_icon=ft.Icons.SEARCH,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12)
        )
        
        search_container = ft.Container(
            content=self.search_input,
            width=600,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                offset=ft.Offset(0, 2)
            ),
            margin=ft.margin.only(bottom=24),
        )

        # Statistics row
        self.stats_row = ft.Row(
            controls=[],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        )

        # Table container
        self.students_table = ft.Column(
            controls=[],
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
        )

        self.update_table()
        self.update_stats()

        # Main content with modern styling
        main_content = ft.Container(
            content=ft.Column([
                title_container,
                
                # Search section
                ft.Container(
                    content=search_container,
                    alignment=ft.alignment.center
                ),
                
                # Statistics section
                ft.Container(
                    content=self.stats_row,
                    margin=ft.margin.only(bottom=24)
                ),
                
                # Table section with modern card styling
                ft.Container(
                    content=ft.Column([
                        self.students_table,
                    ], scroll=ft.ScrollMode.AUTO),
                    bgcolor=ft.Colors.WHITE,
                    border_radius=12,
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=20,
                        color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                        offset=ft.Offset(0, 4)
                    ),
                    border=ft.border.all(1, ft.Colors.with_opacity(0.1, ft.Colors.GREY_400)),
                    expand=True,
                    clip_behavior=ft.ClipBehavior.HARD_EDGE
                ),
            ], 
            spacing=0,
            expand=True
            ),
            padding=ft.padding.all(24),
            expand=True,
            bgcolor=ft.Colors.with_opacity(0.3, ft.Colors.BLUE_GREY_50),
        )

        return main_content