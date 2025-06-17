import flet as ft
from typing import List, Dict, Any


class StudentsTable:
    """Students table component"""

    def __init__(self):
        self.table_container = ft.Column(controls=[], spacing=0, scroll=ft.ScrollMode.AUTO)

    def create_header(self) -> ft.Container:
        """Create table header row"""
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

                ft.Container(
                    content=ft.Text("אחות בחוג", size=14, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE),
                    expand=1,
                    **header_style
                ),
            ], spacing=0),
            border_radius=ft.border_radius.only(top_left=12, top_right=12),
        )

    def create_row(self, student: Dict[str, Any], index: int) -> ft.Container:
        """Create a table row for a student"""
        row_color = ft.Colors.with_opacity(0.3, ft.Colors.BLUE_GREY_50) if index % 2 == 0 else ft.Colors.WHITE

        # Payment status styling
        payment_status = student.get("payment_status", "")
        payment_color, payment_bg, payment_icon = self._get_payment_style(payment_status)

        cell_style = {
            "bgcolor": row_color,
            "padding": ft.padding.symmetric(horizontal=16, vertical=16),
            "alignment": ft.alignment.center,
        }


        has_sister = student.get("has_sister", False)
        sister_mark = "✔" if has_sister else "✘"
        sister_color = ft.Colors.GREEN_700 if has_sister else ft.Colors.RED_700

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
                # הוספת עמודת אחות בחוג
                ft.Container(
                    content=ft.Text(
                        sister_mark,
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=sister_color,
                        text_align=ft.TextAlign.CENTER
                    ),
                    expand=1,
                    **cell_style
                ),
            ], spacing=0),
            border=ft.border.only(bottom=ft.BorderSide(1, ft.Colors.with_opacity(0.1, ft.Colors.GREY_400))),
        )

    def _get_payment_style(self, payment_status: str):
        """Get payment status styling"""
        if payment_status == "שולם":
            return ft.Colors.GREEN_600, ft.Colors.with_opacity(0.1, ft.Colors.GREEN_600), ft.Icons.CHECK_CIRCLE
        elif payment_status == "לא שולם" or payment_status == "ממתין":
            return ft.Colors.ORANGE_600, ft.Colors.with_opacity(0.1, ft.Colors.ORANGE_600), ft.Icons.PENDING
        else:
            return ft.Colors.GREY_600, ft.Colors.with_opacity(0.1, ft.Colors.GREY_600), ft.Icons.HELP

    def update(self, students: List[Dict[str, Any]]):
        """Update table with students data"""
        self.table_container.controls = [self.create_header()]

        if students:
            for index, student in enumerate(students):
                self.table_container.controls.append(self.create_row(student, index))

    def get_container(self) -> ft.Container:
        """Get the table container"""
        return ft.Container(
            content=ft.Column([self.table_container], scroll=ft.ScrollMode.AUTO),
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            border=ft.border.all(1, ft.Colors.with_opacity(0.1, ft.Colors.GREY_400)),
            expand=True,
            clip_behavior=ft.ClipBehavior.HARD_EDGE
        )
