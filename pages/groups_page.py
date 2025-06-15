import json
import flet as ft
from pages.students_page import StudentsPage
from pages.add_group_page import AddGroupPage

class GroupsPage:
    def __init__(self, page, navigation_callback):
        self.page = page
        self.navigation_callback = navigation_callback
        self.add_group_page = None
        
        self.groups_container = ft.Column(
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )
        
        self.scroll_area = ft.Container(
            content=self.groups_container,
            expand=True,
            padding=ft.padding.symmetric(horizontal=20)
        )
        
        self.main_layout = ft.Column(
            controls=[
                self.create_header(),
                self.scroll_area,
                self.create_footer()
            ],
            expand=True,
            spacing=0
        )
        
        self.build_group_buttons()

    def create_header(self):
        """Create clean header section"""
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Column([
                        ft.Text(
                            "ניהול קבוצות",
                            size=28,
                            weight=ft.FontWeight.BOLD,
                            color="#1a202c"
                        ),
                        ft.Text(
                            "כל הקבוצות הפעילות במערכת",
                            size=16,
                            color="#718096"
                        ),
                    ], spacing=4, expand=True),
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.ADD, size=18, color="white"),
                            ft.Text("הוסף קבוצה", color="white", size=14, weight=ft.FontWeight.W_500)
                        ], spacing=8, tight=True),
                        bgcolor="#4299e1",
                        color="white",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            padding=ft.padding.symmetric(horizontal=16, vertical=12),
                            elevation=0,
                        ),
                        on_click=self.add_group_page_func
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(color="#e2e8f0", height=1),
            ], spacing=20),
            padding=ft.padding.all(30),
            bgcolor="white"
        )

    def create_footer(self):
        """Create footer with back button"""
        return ft.Container(
            content=ft.Row([
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Icon(ft.Icons.ARROW_BACK, size=18, color="#4299e1"),
                        ft.Text("חזרה לעמוד הראשי", color="#4299e1", size=14, weight=ft.FontWeight.W_500)
                    ], spacing=8, tight=True),
                    bgcolor="white",
                    color="#4299e1",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        padding=ft.padding.symmetric(horizontal=16, vertical=12),
                        elevation=0,
                        side=ft.BorderSide(width=1, color="#e2e8f0")
                    ),
                    on_click=lambda e: self.go_home()
                )
            ], alignment=ft.MainAxisAlignment.CENTER),
            padding=ft.padding.all(30),
            bgcolor="white"
        )

    def create_group_card(self, group):
        """Create a modern group card"""
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.GROUP, size=24, color="#4299e1"),
                        bgcolor="#ebf8ff",
                        border_radius=12,
                        padding=ft.padding.all(12),
                    ),
                    ft.Column([
                        ft.Text(
                            group["name"],
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color="#1a202c"
                        ),
                        ft.Text(
                            f"מורה: {group.get('teacher', 'לא צוין')}",
                            size=14,
                            color="#718096"
                        ),
                        ft.Text(
                            f"גילאים: {group.get('age_group', 'לא צוין')}",
                            size=14,
                            color="#718096"
                        ),
                    ], spacing=4, expand=True),
                    ft.Column([
                        ft.Text(
                            f"₪{group.get('price', '0')}",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color="#48bb78"
                        ),
                        ft.Container(
                            content=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=16, color="#cbd5e0"),
                            padding=ft.padding.all(4),
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.END, spacing=8),
                ], spacing=16, alignment=ft.MainAxisAlignment.START),
            ], spacing=0),
            bgcolor="white",
            border_radius=12,
            padding=ft.padding.all(20),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.06, ft.Colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
            on_click=lambda e, name=group["name"]: self.show_students(name),
            ink=True,
        )

    def get_view(self):
        return self.main_layout

    def build_group_buttons(self):
        self.groups_container.controls.clear()

        try:
            with open("data/groups.json", encoding="utf-8") as f:
                data = json.load(f)
                groups = data.get("groups", [])
        except Exception as e:
            groups = []
            error_container = ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.ERROR_OUTLINE, size=48, color="#f56565"),
                    ft.Text(
                        "שגיאה בטעינת קבוצות",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color="#1a202c"
                    ),
                    ft.Text(
                        "אנא נסה שוב מאוחר יותר",
                        size=14,
                        color="#718096"
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12),
                padding=ft.padding.all(40),
                alignment=ft.alignment.center,
            )
            self.groups_container.controls.append(error_container)
            print("Error reading JSON file:", e)
            if hasattr(self, 'page'):
                self.page.update()
            return

        if not groups:
            empty_state = ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.GROUP_OFF, size=64, color="#cbd5e0"),
                    ft.Text(
                        "אין קבוצות במערכת",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color="#1a202c"
                    ),
                    ft.Text(
                        "התחל על ידי הוספת הקבוצה הראשונה שלך",
                        size=14,
                        color="#718096",
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.ADD, size=18, color="white"),
                            ft.Text("הוסף קבוצה ראשונה", color="white", size=14, weight=ft.FontWeight.W_500)
                        ], spacing=8, tight=True),
                        bgcolor="#4299e1",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            padding=ft.padding.symmetric(horizontal=20, vertical=12),
                            elevation=0,
                        ),
                        on_click=self.add_group_page_func
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=16),
                padding=ft.padding.all(60),
                alignment=ft.alignment.center,
            )
            self.groups_container.controls.append(empty_state)
        else:
            max_cols = 2  
            rows = []
            current_row = []
            
            for i, group in enumerate(groups):
                group_card = self.create_group_card(group)
                current_row.append(ft.Container(content=group_card, expand=True))
                
                if len(current_row) >= max_cols or i == len(groups) - 1:
                    while len(current_row) < max_cols:
                        current_row.append(ft.Container(expand=True))
                    
                    row_container = ft.Row(
                        controls=current_row.copy(),
                        spacing=20
                    )
                    rows.append(row_container)
                    current_row.clear()
            
            self.groups_container.controls.extend(rows)
        
        if hasattr(self, 'page'):
            self.page.update()

    def show_students(self, group_name):
        students_page = StudentsPage(self.page, self.navigation_callback, group_name)
        self.navigation_callback(students_page)

    def go_home(self):
        self.navigation_callback(None, 0) 

    def add_group_page_func(self, e=None):
        self.add_group_page = AddGroupPage(self.page, self.navigation_callback, self)
        self.navigation_callback(self.add_group_page)

    def refresh(self):
        self.build_group_buttons()

    def clear_layout(self):
        pass
