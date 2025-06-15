import flet as ft
from components.modern_card import ModernCard
from components.clean_button import CleanButton


class StudentsGroupView:
    """View for displaying students list"""
    
    def __init__(self, parent):
        self.parent = parent
        self.page = parent.page
        self.group_name = parent.group_name
        self.data_manager = parent.data_manager

    def render(self):
        """Render the students list view"""
        # Header
        header = self._create_header()
        self.parent.layout.controls.append(header)
        
        # Load students
        students = self.data_manager.get_students_by_group(self.group_name)
        
        if not students:
            self._render_empty_state()
        else:
            self._render_students_grid(students)
        
        # Action buttons
        actions = self._create_action_buttons()
        self.parent.layout.controls.append(actions)
        
        self.page.update()

    def _create_header(self):
        """Create page header"""
        return ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.PEOPLE_ALT_OUTLINED, size=24, color=ft.Colors.GREY_800),
                ft.Text(
                    f"תלמידות - {self.group_name}",
                    size=24,
                    weight=ft.FontWeight.W_600,
                    color=ft.Colors.GREY_800,
                ),
            ], spacing=12),
            padding=ft.padding.symmetric(vertical=16)
        )

    def _render_empty_state(self):
        """Render empty state when no students"""
        empty_state = ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.PERSON_ADD_ALT_1_OUTLINED, size=48, color=ft.Colors.GREY_400),
                ft.Text(
                    "אין תלמידות בקבוצה זו",
                    size=18,
                    weight=ft.FontWeight.W_500,
                    color=ft.Colors.GREY_600,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    "הוסיפו את התלמידה הראשונה",
                    size=14,
                    color=ft.Colors.GREY_500,
                    text_align=ft.TextAlign.CENTER
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
            padding=ft.padding.all(48),
            alignment=ft.alignment.center
        )
        self.parent.layout.controls.append(empty_state)

    def _render_students_grid(self, students):
        """Render students in a responsive grid"""
        # Students count
        count_text = ft.Container(
            content=ft.Text(
                f"{len(students)} תלמידות",
                size=14,
                color=ft.Colors.GREY_600
            ),
            padding=ft.padding.only(bottom=16)
        )
        self.parent.layout.controls.append(count_text)
        
        # Create responsive grid
        students_grid = ft.Container(
            content=ft.Column([
                ft.ResponsiveRow([
                    ft.Container(
                        content=self._create_student_card(student),
                        col={"xs": 12, "sm": 6, "md": 4, "lg": 3}
                    )
                    for student in students
                ], spacing=16, run_spacing=16)
            ], scroll=ft.ScrollMode.AUTO),
        )
        self.parent.layout.controls.append(students_grid)

    def _create_student_card(self, student):
        """Create a student card"""
        # Avatar
        avatar = ft.Container(
            content=ft.Text(
                student['name'][0] if student['name'] else "?",
                color=ft.Colors.WHITE,
                size=16,
                weight=ft.FontWeight.W_600,
                text_align=ft.TextAlign.CENTER
            ),
            bgcolor=ft.Colors.BLUE_600,
            border_radius=20,
            width=36,
            height=36,
            alignment=ft.alignment.center,
        )
        
        # Payment status
        payment_status = student.get('payment_status', '')
        status_color = self._get_payment_status_color(payment_status)
        
        status_dot = ft.Container(
            width=8,
            height=8,
            bgcolor=status_color,
            border_radius=4
        )
        
        # Card content
        card_content = ft.Column([
            # Header
            ft.Row([
                avatar,
                ft.Column([
                    ft.Text(
                        student['name'],
                        size=16,
                        weight=ft.FontWeight.W_600,
                        color=ft.Colors.GREY_800,
                        overflow=ft.TextOverflow.ELLIPSIS
                    ),
                    ft.Row([
                        status_dot,
                        ft.Text(
                            payment_status,
                            size=12,
                            color=ft.Colors.GREY_600,
                            overflow=ft.TextOverflow.ELLIPSIS
                        )
                    ], spacing=6)
                ], spacing=2, expand=True)
            ], spacing=12),
            
            # Contact info
            self._create_contact_info(student),
            
            # Action buttons
            self._create_card_actions(student)
        ], spacing=12)
        
        return ModernCard(
            content=ft.Container(
                content=card_content,
                padding=ft.padding.all(16)
            ),
            hover_effect=True
        )

    def _create_contact_info(self, student):
        """Create contact information section"""
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.PHONE, size=14, color=ft.Colors.GREY_500),
                    ft.Text(
                        student.get('phone', 'לא צוין'),
                        size=12,
                        color=ft.Colors.GREY_600,
                        overflow=ft.TextOverflow.ELLIPSIS
                    )
                ], spacing=6),
                ft.Row([
                    ft.Icon(ft.Icons.CALENDAR_TODAY, size=14, color=ft.Colors.GREY_500),
                    ft.Text(
                        student.get('join_date', 'לא ידוע'),
                        size=12,
                        color=ft.Colors.GREY_600,
                        overflow=ft.TextOverflow.ELLIPSIS
                    )
                ], spacing=6)
            ], spacing=4),
            padding=ft.padding.symmetric(vertical=8)
        )

    def _create_card_actions(self, student):
        """Create action buttons for student card"""
        return ft.Row([
            CleanButton.create_icon_button(
                ft.Icons.EDIT_OUTLINED,
                ft.Colors.GREY_600,
                "עריכה",
                lambda e: self.parent.edit_student(student)
            ),
            CleanButton.create_icon_button(
                ft.Icons.PAYMENT_OUTLINED,
                ft.Colors.GREY_600,
                "תשלומים",
                lambda e: self.parent.show_payments(student)
            ),
            CleanButton.create_icon_button(
                ft.Icons.DELETE_OUTLINE,
                ft.Colors.RED_400,
                "מחיקה",
                lambda e: self.parent.delete_student(student['name']),
                ft.Colors.RED_50
            )
        ], spacing=4, alignment=ft.MainAxisAlignment.END)

    def _create_action_buttons(self):
        """Create main action buttons"""
        return ft.Container(
            content=ft.Row([
                CleanButton.create(
                    "הוסף תלמידה",
                    ft.Icons.ADD,
                    ft.Colors.BLUE_600,
                    self.parent.go_to_add_student_page
                ),
                CleanButton.create(
                    "חזרה",
                    ft.Icons.ARROW_BACK,
                    ft.Colors.GREY_600,
                    self.parent.go_back,
                    variant="outlined"
                )
            ], spacing=16, alignment=ft.MainAxisAlignment.CENTER),
            padding=ft.padding.symmetric(vertical=24)
        )

    def _get_payment_status_color(self, payment_status):
        """Get color for payment status"""
        if payment_status == "שולם":
            return ft.Colors.GREEN_600
        elif "חוב" in payment_status:
            return ft.Colors.RED_500
        else:
            return ft.Colors.ORANGE_500
