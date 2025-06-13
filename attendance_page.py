import json
import flet as ft
from typing import List, Dict, Any, Optional

def load_groups():
    """Load groups from JSON file"""
    try:
        with open("data/groups.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            return data.get("groups", [])
    except Exception as e:
        print("Error on Load groups", e)
        return []

class AttendancePage:
    def __init__(self, page: ft.Page, navigation_handler=None):
        self.page = page
        self.navigation_handler = navigation_handler
        self.groups = []
        
        # Load groups data
        self.refresh_data()

    def refresh_data(self):
        """Refresh groups data"""
        self.groups = load_groups()

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
                "ניהול נוכחות",
                size=24,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_GREY_800,
                text_align=ft.TextAlign.CENTER,
                rtl=True
            ),
            ft.Text(
                "בחר קבוצה לניהול נוכחות",
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

    def show_group_attendance(self, group):
        """Show attendance for selected group"""
        from attendance_table_page import GroupAttendancePage  # שנה את זה
        attendance_page = GroupAttendancePage(self.page, self.navigation_handler, group)  # שנה את זה
        self.navigation_handler(attendance_page, None)


    def create_enhanced_group_button(self, group: Dict[str, Any], index: int):
        """Create an enhanced group button with hover effects"""
        def on_group_click(e):
            self.show_group_attendance(group)

        def on_hover(e):
            if e.data == "true":
                e.control.bgcolor = ft.Colors.LIGHT_BLUE_200
                e.control.scale = 1.02
            else:
                e.control.bgcolor = ft.Colors.LIGHT_BLUE_100
                e.control.scale = 1.0
            e.control.update()

        # Add some group info if available
        group_info = []
        if group.get("description"):
            group_info.append(
                ft.Text(
                    group["description"],
                    size=12,
                    color=ft.Colors.GREY_600,
                    text_align=ft.TextAlign.CENTER,
                    rtl=True
                )
            )

        button_content = ft.Column([
            ft.Text(
                group.get("name", ""),
                size=14,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_GREY_800,
                text_align=ft.TextAlign.CENTER,
                rtl=True
            ),
            *group_info,
            ft.Row([
                ft.Icon(ft.Icons.ARROW_FORWARD, size=16, color=ft.Colors.BLUE_600),
                ft.Text(
                    "לחץ לניהול נוכחות",
                    size=12,
                    color=ft.Colors.BLUE_600,
                    rtl=True
                )
            ], 
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=5
            )
        ], 
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=5,
        tight=True
        )

        return ft.Container(
            content=button_content,
            bgcolor=ft.Colors.LIGHT_BLUE_100,
            border_radius=6,
            padding=ft.padding.all(12),
            margin=ft.margin.symmetric(vertical=2),
            on_click=on_group_click,
            on_hover=on_hover,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
            animate_scale=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
            ink=True,
        )

    def create_enhanced_groups_card(self):
        """Create enhanced groups selection card with better styling"""
        if not self.groups:
            # Empty state with action button
            def refresh_groups(e):
                self.refresh_data()
                # Refresh the view
                if hasattr(self, '_main_content'):
                    self._main_content.content = self._create_main_content()
                    self.page.update()

            empty_content = ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.GROUP, size=64, color=ft.Colors.GREY_400),
                    ft.Text(
                        "אין קבוצות זמינות",
                        size=16,
                        color=ft.Colors.GREY_600,
                        text_align=ft.TextAlign.CENTER,
                        rtl=True
                    ),
                    ft.Text(
                        "הוסף קבוצות כדי להתחיל לנהל נוכחות",
                        size=14,
                        color=ft.Colors.GREY_500,
                        text_align=ft.TextAlign.CENTER,
                        rtl=True
                    ),
                    ft.ElevatedButton(
                        text="רענן רשימת קבוצות",
                        on_click=refresh_groups,
                        bgcolor=ft.Colors.BLUE_600,
                        color=ft.Colors.WHITE,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=6),
                        ),
                    )
                ], 
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15
                ),
                padding=ft.padding.all(40),
                alignment=ft.alignment.center,
            )
            return self.create_animated_card(empty_content)

        # Create enhanced group buttons
        group_buttons = []
        for index, group in enumerate(self.groups):
            group_buttons.append(self.create_enhanced_group_button(group, index))

        # Header for groups section
        groups_header = ft.Row([
            ft.Icon(ft.Icons.GROUP, size=20, color=ft.Colors.BLUE_600),
            ft.Text(
                f"קבוצות זמינות ({len(self.groups)})",
                size=16,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_GREY_800,
                rtl=True
            )
        ], 
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=8
        )

        # Create scrollable container for groups
        groups_content = ft.Column([
            groups_header,
            ft.Divider(height=1, color=ft.Colors.GREY_300),
            ft.Container(
                content=ft.Column(
                    controls=group_buttons,
                    spacing=8,
                    scroll=ft.ScrollMode.AUTO,
                ),
                height=350,  # Fixed height to enable scrolling
                padding=ft.padding.all(5),
            )
        ], spacing=10)

        return self.create_animated_card(groups_content)

    def go_home(self, e):
        """Navigate back to home page"""
        if self.navigation_handler:
            self.navigation_handler(None, 0)  # Navigate to dashboard (index 0)

    def create_navigation_card(self):
        """Create the navigation card with back button"""
        back_button = ft.ElevatedButton(
            text="⬅ חזרה לעמוד הראשי",
            on_click=self.go_home,
            bgcolor=ft.Colors.RED_600,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=6),
                padding=ft.padding.symmetric(horizontal=20, vertical=12),
            ),
            height=40,
        )

        nav_content = ft.Row([
            back_button
        ], 
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10
        )

        return self.create_animated_card(nav_content)

    def _create_main_content(self):
        """Create the main content structure"""
        return ft.Column([
            self.create_header_card(),
            self.create_enhanced_groups_card(),
            self.create_navigation_card(),
        ], 
        spacing=20,
        expand=True
        )

    def get_view(self):
        """Get the main view of the attendance page"""
        # Create main content
        main_content_column = self._create_main_content()

        # Main container
        self._main_content = ft.Container(
            content=main_content_column,
            padding=ft.padding.all(30),
            bgcolor=ft.Colors.GREY_50,
            expand=True,
        )

        return self._main_content
