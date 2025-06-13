import flet as ft
import os
import asyncio
from typing import Optional
import math
from attendance_page import AttendancePage
from groups_page import GroupsPage  
from students_list import StudentsListPage
from payment_page import PaymentPage
from group_attendance_page import GroupAttendancePage
from data_utils import get_all_dashboard_data

def format_currency(amount):
    return f"₪{amount:,}"


class MainApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "זה הריקוד שלך"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.window_width = 1200
        self.page.window_height = 800
        self.page.window_min_width = 1000
        self.page.window_min_height = 700
        self.page.rtl = True
        self.page.fonts = {
            "Segoe UI": "fonts/SegoeUI.ttf" if os.path.exists("fonts/SegoeUI.ttf") else None
        }
        self.dashboard_data = get_all_dashboard_data()
        self.current_page_index = 0
        self.sidebar_buttons = []
        self.progress_bar = None
        self.progress_text = None
        self.groups_page = None
        self.setup_page()

    def setup_page(self):
        self.sidebar = self.create_sidebar()
        self.content_area = ft.Container(
            content=self.create_home_page(),
            bgcolor="#f8fafc",
            expand=True,
            padding=ft.padding.all(30),
        )
        
        main_row = ft.Row([
            self.sidebar,
            self.content_area
        ], spacing=0, expand=True)
        
        self.page.add(main_row)

    def create_sidebar_button(self, text: str, icon: str, index: int, is_selected: bool = False):
        """Create an animated sidebar button using built-in Flet components"""
        
        def on_click(e):
            self.navigate_to_page(index)
        
        button_content = ft.Row([
            ft.Icon(
                icon,
                color=ft.Colors.WHITE if is_selected else ft.Colors.GREY_400,
                size=20
            ),
            ft.Text(
                text,
                color=ft.Colors.WHITE if is_selected else ft.Colors.GREY_400,
                size=14,
                weight=ft.FontWeight.BOLD if is_selected else ft.FontWeight.NORMAL
            )
        ], spacing=10)
        
        button_container = ft.Container(
            content=button_content,
            padding=ft.padding.all(12),
            border_radius=8,
            bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE) if is_selected else None,
            on_click=on_click,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
            ink=True,
        )
        
        if is_selected:
            return ft.Row([
                ft.Container(
                    width=4,
                    height=40,
                    bgcolor=ft.Colors.BLUE,
                    border_radius=2,
                ),
                ft.Container(
                    content=button_container,
                    expand=True
                )
            ], spacing=0)
        else:
            return ft.Container(
                content=button_container,
                margin=ft.margin.only(left=4)
            )

    def create_sidebar(self):
        home_btn = self.create_sidebar_button("דף הבית", ft.Icons.HOME, 0, self.current_page_index == 0)
        groups_btn = self.create_sidebar_button("קבוצות", ft.Icons.GROUP, 1, self.current_page_index == 1)
        attendance_btn = self.create_sidebar_button("נוכחות", ft.Icons.CHECK_CIRCLE, 2, self.current_page_index == 2)
        payment_btn = self.create_sidebar_button("תשלומים", ft.Icons.CREDIT_CARD, 3, self.current_page_index == 3)
        students_btn = self.create_sidebar_button("רשימת התלמידות", ft.Icons.LIST, 4, self.current_page_index == 4)

        self.sidebar_buttons = [home_btn, groups_btn, attendance_btn, payment_btn, students_btn]

        def toggle_dark_mode(e):
            self.toggle_dark_mode(e.control.value)
            
        dark_mode_switch = ft.Switch(
            value=False,
            on_change=toggle_dark_mode,
            active_color=ft.Colors.BLUE,
            inactive_thumb_color=ft.Colors.WHITE,
            inactive_track_color=ft.Colors.GREY_400,
        )

        sidebar_content = ft.Column([
            ft.Container(
                content=ft.Text("זה הריקוד שלך", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                padding=ft.padding.all(20),
                alignment=ft.alignment.center,
            ),
            
            ft.Divider(color=ft.Colors.GREY_600, height=1),            
            ft.Container(
                content=ft.Column([
                    home_btn,
                    groups_btn,
                    attendance_btn,
                    payment_btn,
                    students_btn,
                ], spacing=5),
                padding=ft.padding.symmetric(horizontal=10, vertical=20),
            ),
            ft.Container(expand=True),
            ft.Container(
                content=ft.Column([
                    ft.Text("הגדרות", size=12, color=ft.Colors.GREY_500),
                    ft.Row([
                        dark_mode_switch,
                        ft.Text("מצב כהה", color=ft.Colors.GREY_400),
                    ], spacing=10),
                ], spacing=10),
                padding=ft.padding.all(20),
            ),
        ], spacing=0)

        return ft.Container(
            content=sidebar_content,
            width=250,
            bgcolor="#2c3e50",
            height=self.page.window_height,
        )

    def navigate_to_page(self, page_index: int):
        """Navigate to a specific page"""
        self.current_page_index = page_index
        self.sidebar.content = self.create_sidebar().content
        if page_index == 0:
            self.content_area.content = self.create_home_page()
            self.refresh_home_page()
        elif page_index == 1:
            if self.groups_page is None:
                self.groups_page = GroupsPage(self.page, self.handle_navigation)
            self.content_area.content = self.groups_page.get_view()
        elif page_index == 2:
            attendance_page = AttendancePage(self.page, self.handle_navigation)
            self.content_area.content = attendance_page.get_view()
        elif page_index == 3:
            payment_page = PaymentPage(self.page, self.handle_navigation)
            self.content_area.content = payment_page.get_view()
        elif page_index == 4:
            students_page = StudentsListPage(self.page, self.handle_navigation)
            self.content_area.content = students_page.get_view()
        self.page.update()

    def handle_navigation(self, page_instance, page_index=None):
        """Handle navigation from sub-pages"""
        if page_index is not None:
            self.navigate_to_page(page_index)
        elif page_instance is not None:
            self.content_area.content = page_instance.get_view()
            self.page.update()

    def create_placeholder_page(self, title: str):
        """Create placeholder page for non-implemented pages"""
        return ft.Column([
            ft.Text(f"עמוד {title}", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("עמוד זה יומר בהמשך", size=16, color=ft.Colors.GREY_600),
        ], spacing=20)

    def create_animated_card(self, content, height: Optional[int] = None, width: Optional[int] = None, gradient_colors=None, on_click=None):
        """Create an animated card using built-in Flet components"""
        return ft.Container(
            content=content,
            bgcolor=ft.Colors.WHITE if not gradient_colors else None,
            gradient=ft.LinearGradient(
                colors=gradient_colors,
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
            ) if gradient_colors else None,
            border_radius=12,
            padding=ft.padding.all(20),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=10,
                color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                offset=ft.Offset(0, 4),
            ),
            height=height,
            width=width,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
            on_click=on_click,
            ink=True if on_click else False,
        )

    def create_home_page(self):
        # כותרת פשוטה ונקייה
        welcome_section = ft.Container(
            content=ft.Column([
                ft.Text(
                    "ברוכים הבאים לזה הריקוד שלך", 
                    size=32, 
                    weight=ft.FontWeight.BOLD, 
                    color="#1a202c"
                ),
                ft.Text(
                    "הבית המקצועי לבלט ולמחול", 
                    size=16, 
                    color="#718096"
                ),
            ], spacing=8),
            padding=ft.padding.only(bottom=30),
        )

        # כרטיסי סטטיסטיקות
        students_card = self.create_animated_card(
            content=ft.Column([
                ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.PERSON, size=24, color="#4299e1"),
                        bgcolor="#ebf8ff",
                        border_radius=8,
                        padding=ft.padding.all(8),
                    ),
                    ft.Column([
                        ft.Text("תלמידות", size=14, color="#718096"),
                        ft.Text(str(self.dashboard_data['total_students']), size=28, 
                               weight=ft.FontWeight.BOLD, color="#1a202c"),
                    ], spacing=2, expand=True),
                ], spacing=12, alignment=ft.MainAxisAlignment.START),
            ], spacing=5),
            height=100
        )

        groups_card = self.create_animated_card(
            content=ft.Column([
                ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.GROUP, size=24, color="#48bb78"),
                        bgcolor="#f0fff4",
                        border_radius=8,
                        padding=ft.padding.all(8),
                    ),
                    ft.Column([
                        ft.Text("קבוצות פעילות", size=14, color="#718096"),
                        ft.Text(str(self.dashboard_data['total_groups']), size=28, 
                               weight=ft.FontWeight.BOLD, color="#1a202c"),
                    ], spacing=2, expand=True),
                ], spacing=12, alignment=ft.MainAxisAlignment.START),
            ], spacing=5),
            height=100
        )

        payments_card = self.create_animated_card(
            content=ft.Column([
                ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET, size=24, color="#ed8936"),
                        bgcolor="#fffaf0",
                        border_radius=8,
                        padding=ft.padding.all(8),
                    ),
                    ft.Column([
                        ft.Text("הכנסות החודש", size=14, color="#718096"),
                        ft.Text(format_currency(self.dashboard_data['monthly_payments']), size=24, 
                               weight=ft.FontWeight.BOLD, color="#1a202c"),
                    ], spacing=2, expand=True),
                ], spacing=12, alignment=ft.MainAxisAlignment.START),
            ], spacing=5),
            height=100
        )

        attendance_card = self.create_animated_card(
            content=ft.Column([
                ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.ANALYTICS, size=24, color="#9f7aea"),
                        bgcolor="#faf5ff",
                        border_radius=8,
                        padding=ft.padding.all(8),
                    ),
                    ft.Column([
                        ft.Text("נוכחות חודשית", size=14, color="#718096"),
                        ft.Text(f"{self.dashboard_data['attendance_percentage']}%", size=28, 
                               weight=ft.FontWeight.BOLD, color="#1a202c"),
                    ], spacing=2, expand=True),
                ], spacing=12, alignment=ft.MainAxisAlignment.START),
            ], spacing=5),
            height=100
        )

        # רשת הכרטיסים
        stats_grid = ft.Row([
            ft.Container(content=students_card, expand=1),
            ft.Container(content=groups_card, expand=1),
            ft.Container(content=payments_card, expand=1),
            ft.Container(content=attendance_card, expand=1),
        ], spacing=20)

        # פעולות מהירות במרכז
        def navigate_to_students(e):
            self.navigate_to_page(4)
            
        def navigate_to_attendance(e):
            self.navigate_to_page(2)
            
        def navigate_to_payments(e):
            self.navigate_to_page(3)
            
        def navigate_to_groups(e):
            self.navigate_to_page(1)

        quick_actions = ft.Container(
            content=ft.Column([
                ft.Text("פעולות מהירות", size=24, weight=ft.FontWeight.BOLD, color="#1a202c"),
                ft.Row([
                    self.create_animated_card(
                        content=ft.Column([
                            ft.Container(
                                content=ft.Icon(ft.Icons.PERSON_ADD, size=32, color="#4299e1"),
                                bgcolor="#ebf8ff",
                                border_radius=12,
                                padding=ft.padding.all(12),
                            ),
                            ft.Text("הוספת תלמידה", size=16, weight=ft.FontWeight.W_500, 
                                   text_align=ft.TextAlign.CENTER, color="#1a202c"),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12),
                        height=120,
                        on_click=navigate_to_students,
                    ),
                    self.create_animated_card(
                        content=ft.Column([
                            ft.Container(
                                content=ft.Icon(ft.Icons.CHECK_CIRCLE, size=32, color="#48bb78"),
                                bgcolor="#f0fff4",
                                border_radius=12,
                                padding=ft.padding.all(12),
                            ),
                            ft.Text("סימון נוכחות", size=16, weight=ft.FontWeight.W_500, 
                                   text_align=ft.TextAlign.CENTER, color="#1a202c"),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12),
                        height=120,
                        on_click=navigate_to_attendance,
                    ),
                    self.create_animated_card(
                        content=ft.Column([
                            ft.Container(
                                content=ft.Icon(ft.Icons.PAYMENT, size=32, color="#ed8936"),
                                bgcolor="#fffaf0",
                                border_radius=12,
                                padding=ft.padding.all(12),
                            ),
                            ft.Text("רישום תשלום", size=16, weight=ft.FontWeight.W_500, 
                                   text_align=ft.TextAlign.CENTER, color="#1a202c"),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12),
                        height=120,
                        on_click=navigate_to_payments,
                    ),
                    self.create_animated_card(
                        content=ft.Column([
                            ft.Container(
                                content=ft.Icon(ft.Icons.GROUP, size=32, color="#9f7aea"),
                                bgcolor="#faf5ff",
                                border_radius=12,
                                padding=ft.padding.all(12),
                            ),
                            ft.Text("ניהול קבוצות", size=16, weight=ft.FontWeight.W_500, 
                                   text_align=ft.TextAlign.CENTER, color="#1a202c"),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12),
                        height=120,
                        on_click=navigate_to_groups,
                    ),
                ], spacing=20, alignment=ft.MainAxisAlignment.CENTER),
            ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.symmetric(vertical=30),
        )

        return ft.Column([
            welcome_section,
            stats_grid,
            quick_actions,
        ], spacing=40, scroll=ft.ScrollMode.AUTO)

    def refresh_home_page(self):
        """Refresh home page data"""
        try:
            self.dashboard_data = get_all_dashboard_data()
            if self.current_page_index == 0:
                self.content_area.content = self.create_home_page()
                self.content_area.update()
        except Exception as e:
            print(f"שגיאה בעדכון עמוד הבית: {e}")

    def toggle_dark_mode(self, enabled: bool):
        """Toggle between light and dark mode"""
        if enabled:
            self.page.theme_mode = ft.ThemeMode.DARK
            self.content_area.bgcolor = "#1a1a1a"
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self.content_area.bgcolor = "#f8fafc"
        
        self.page.update()

def main(page: ft.Page):
    app = MainApp(page)

if __name__ == '__main__':
    ft.app(target=main)
