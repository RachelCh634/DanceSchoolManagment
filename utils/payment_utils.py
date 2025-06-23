import json
import os
from datetime import datetime, timedelta

class PaymentCalculator:
    def __init__(self):
        self.groups_file_path = "data/groups.json"
        self.students_file_path = "data/students.json"  # נוסיף נתיב לקובץ התלמידות
    
    def load_groups(self):
        """Load groups data from JSON file"""
        try:
            if os.path.exists(self.groups_file_path):
                with open(self.groups_file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("groups", [])
            return []
        except Exception as e:
            print(f"Error loading groups: {e}")
            return []
    
    def load_students(self):
        """Load students data from JSON file"""
        try:
            if os.path.exists(self.students_file_path):
                with open(self.students_file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("students", [])
            return []
        except Exception as e:
            print(f"Error loading students: {e}")
            return []
    
    def get_student_by_id(self, student_id):
        """Get student details by ID"""
        students = self.load_students()
        for student in students:
            if student.get("id") == student_id:
                return student
        return None
    
    def calculate_multiple_groups_discount(self, base_price, num_groups):
        """
        Calculate discounted price for multiple groups
        - 1 group: regular price (180)
        - 2 groups: 280 total (instead of 360)
        - 3 groups: 380 total (instead of 540)
        """
        if num_groups == 1:
            return base_price
        elif num_groups == 2:
            return 280
        elif num_groups >= 3:
            return 380
        else:
            return base_price
    
    def calculate_sister_discount(self, price, has_sister):
        """
        Apply sister discount - 20 NIS less per month if has sister
        """
        if has_sister:
            return max(0, price - 20)  # מוודא שהמחיר לא יהיה שלילי
        return price
    
    def calculate_monthly_price_with_discounts(self, student_id, base_price=180):
        """
        Calculate monthly price with all applicable discounts
        
        Args:
            student_id (str): ID of the student
            base_price (float): Base price per group (default 180)
            
        Returns:
            dict: Price calculation details with discounts
        """
        try:
            student = self.get_student_by_id(student_id)
            if not student:
                return {
                    "success": False,
                    "error": f"Student with ID {student_id} not found"
                }
            
            # Get number of groups
            groups = student.get("groups", [])
            num_groups = len(groups)
            
            if num_groups == 0:
                return {
                    "success": False,
                    "error": "Student is not enrolled in any groups"
                }
            
            # Calculate price with multiple groups discount
            price_after_groups_discount = self.calculate_multiple_groups_discount(base_price, num_groups)
            
            # Apply sister discount
            has_sister = student.get("has_sister", False)
            final_price = self.calculate_sister_discount(price_after_groups_discount, has_sister)
            
            return {
                "success": True,
                "student_name": student.get("name", ""),
                "student_id": student_id,
                "num_groups": num_groups,
                "groups": groups,
                "base_price": base_price,
                "price_before_discounts": base_price * num_groups,
                "price_after_groups_discount": price_after_groups_discount,
                "has_sister": has_sister,
                "sister_discount": 20 if has_sister else 0,
                "final_monthly_price": final_price,
                "total_discount": (base_price * num_groups) - final_price
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error calculating monthly price with discounts: {str(e)}"
            }
    
    def get_group_by_id(self, group_id):
        """Get group details by ID"""
        groups = self.load_groups()
        for group in groups:
            if group.get("id") == group_id:
                return group
        return None
    
    def get_group_id_by_name(self, group_name):
        """Get group ID by group name"""
        groups = self.load_groups()
        for group in groups:
            if group.get("name") == group_name:
                return group.get("id")
        return None

    def get_end_of_month(self, date):
        """Get the last day of the month for given date"""
        if isinstance(date, str):
            date = datetime.strptime(date, "%d/%m/%Y")
        
        # Get the first day of next month, then subtract one day
        if date.month == 12:
            next_month = date.replace(year=date.year + 1, month=1, day=1)
        else:
            next_month = date.replace(month=date.month + 1, day=1)
        
        end_of_month = next_month - timedelta(days=1)
        return end_of_month
    
    def count_meetings_in_date_range(self, group_id, start_date, end_date):
        """Count theoretical meetings in any date range based on course schedule"""
        try:
            # Get group details
            group = self.get_group_by_id(group_id)
            if not group:
                print(f"Group with ID {group_id} not found")
                return 0
            
            # Get course day of week from group data
            course_day = group.get("day_of_week")
            if not course_day:
                print(f"Course day not found for group {group_id}")
                return 0
            
            # Convert Hebrew day names to weekday numbers (0=Monday, 6=Sunday)
            hebrew_days = {
                "ראשון": 6,    # Sunday
                "שני": 0,      # Monday  
                "שלישי": 1,    # Tuesday
                "רביעי": 2,    # Wednesday
                "חמישי": 3,    # Thursday
                "שישי": 4,     # Friday
                "שבת": 5       # Saturday
            }
            
            course_weekday = hebrew_days.get(course_day)
            if course_weekday is None:
                print(f"Invalid course day: {course_day}")
                return 0
            
            # Convert dates to datetime objects if they're strings
            if isinstance(start_date, str):
                start_date = datetime.strptime(start_date, "%d/%m/%Y")
            if isinstance(end_date, str):
                end_date = datetime.strptime(end_date, "%d/%m/%Y")
            
            # Count how many times the course day occurs in the date range
            meetings_count = 0
            current_date = start_date
            
            while current_date <= end_date:
                # Check if current date is the course day
                if current_date.weekday() == course_weekday:
                    meetings_count += 1
                current_date += timedelta(days=1)
            
            return meetings_count
            
        except Exception as e:
            print(f"Error counting meetings in date range: {e}")
            return 0
    
    def calculate_months_between_dates(self, start_date, end_date):
        """
        Calculate number of months between two dates
        FIXED: If end date is the 1st of the month, don't count that month
        """
        try:
            if isinstance(start_date, str):
                start_date = datetime.strptime(start_date, "%d/%m/%Y")
            if isinstance(end_date, str):
                end_date = datetime.strptime(end_date, "%d/%m/%Y")
            
            if end_date.day == 1:
                if end_date.month == 1:
                    end_date = end_date.replace(year=end_date.year - 1, month=12, day=31)
                else:
                    # Go to last day of previous month
                    previous_month = end_date.month - 1
                    # Get last day of previous month
                    if previous_month in [1, 3, 5, 7, 8, 10, 12]:
                        last_day = 31
                    elif previous_month in [4, 6, 9, 11]:
                        last_day = 30
                    else:  # February
                        # Check for leap year
                        year = end_date.year
                        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                            last_day = 29
                        else:
                            last_day = 28
                    
                    end_date = end_date.replace(month=previous_month, day=last_day)
            
            # Calculate difference in months
            months_diff = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
            
            # If end date day is before start date day, subtract one month
            if end_date.day < start_date.day:
                months_diff -= 1
            
            return max(0, months_diff)
            
        except Exception as e:
            print(f"Error calculating months between dates: {e}")
            return 0

    
    def calculate_first_month_payment(self, monthly_price, meetings_attended):
        """
        Calculate first month payment based on meetings attended
        - If 3+ meetings: full monthly price
        - If less than 3: proportional payment (monthly_price / 4 * meetings_attended)
        """
        if meetings_attended >= 3:
            return monthly_price
        else:
            # Proportional payment: monthly price divided by 4, multiplied by meetings attended
            return (monthly_price / 4) * meetings_attended
    
    def _get_student_and_validate(self, student_id):
        """Helper method to get student and calculate their monthly price with discounts"""
        student = self.get_student_by_id(student_id)
        if not student:
            return None, {
                "success": False,
                "error": f"Student with ID {student_id} not found"
            }
        
        # Calculate monthly price with all discounts
        price_calculation = self.calculate_monthly_price_with_discounts(student_id)
        if not price_calculation.get("success"):
            return None, price_calculation
        
        monthly_price = price_calculation["final_monthly_price"]
        
        return student, {
            "monthly_price": monthly_price,
            "price_details": price_calculation
        }
    
    def _get_group_and_validate(self, group_id):
        """Helper method to get group and validate basic requirements (legacy method for backward compatibility)"""
        group = self.get_group_by_id(group_id)
        if not group:
            return None, {
                "success": False,
                "error": f"Group with ID {group_id} not found"
            }
        
        monthly_price = float(group.get("price", 180))  # Default to 180 if no price
        
        return group, {"monthly_price": monthly_price}
    
    def _create_payment_result(self, student_or_group, monthly_price, total_months, first_month_meetings, 
                             first_month_payment, remaining_months, remaining_months_payment,
                             start_date, end_date, payment_type, current_date=None, price_details=None):
        """Helper method to create standardized payment result"""
        total_payment = first_month_payment + remaining_months_payment
        
        # Handle both student and group objects
        if isinstance(student_or_group, dict) and "name" in student_or_group:
            entity_name = student_or_group.get("name", "")
            entity_type = "student"
        else:
            entity_name = student_or_group.get("name", "") if student_or_group else ""
            entity_type = "group"
        
        result = {
            "success": True,
            "entity_name": entity_name,
            "entity_type": entity_type,
            "monthly_price": monthly_price,
            "total_months": total_months,
            "first_month_meetings": first_month_meetings,
            "first_month_full_price": first_month_meetings >= 3,
            "first_month_payment": round(first_month_payment, 2),
            "remaining_months": remaining_months,
            "remaining_months_payment": remaining_months_payment,
            "total_payment": round(total_payment, 2),
            "start_date": start_date,
            "end_date": end_date,
            "calculation_method": "Full price" if first_month_meetings >= 3 else "Proportional (price/4 * meetings)",
            "payment_type": payment_type
        }
        
        if current_date:
            result["current_date"] = current_date
        
        if price_details:
            result["price_details"] = price_details
            
        return result
    
    def calculate_student_payment_until_now(self, student_id, start_date):
        """
        Calculate payment for student from start date until end of current month
        Uses student's discounted monthly price based on number of groups and sister discount
        
        Args:
            student_id (str): ID of the student
            start_date (str): Start date when student joined in format "dd/mm/yyyy"
            
        Returns:
            dict: Payment calculation details until current month end
        """
        try:
            # Get and validate student
            student, validation_result = self._get_student_and_validate(student_id)
            if not student:
                return validation_result
            
            monthly_price = validation_result["monthly_price"]
            price_details = validation_result["price_details"]
            
            # Convert start_date to datetime
            if isinstance(start_date, str):
                start_date_dt = datetime.strptime(start_date, "%d/%m/%Y")
            else:
                start_date_dt = start_date
            
            # Use end of current month
            current_date = datetime.now()
            end_of_current_month = self.get_end_of_month(current_date)
            end_date_str = end_of_current_month.strftime("%d/%m/%Y")
            payment_type = "Until current month end"
            current_date_str = current_date.strftime("%d/%m/%Y")
            
            # If start date is after current date, no payment needed yet
            if start_date_dt > current_date:
                result = {
                    "success": True,
                    "entity_name": student.get("name", ""),
                    "entity_type": "student",
                    "monthly_price": monthly_price,
                    "total_months": 0,
                    "first_month_meetings": 0,
                    "first_month_payment": 0,
                    "remaining_months": 0,
                    "remaining_months_payment": 0,
                    "total_payment": 0,
                    "start_date": start_date,
                    "current_date": current_date_str,
                    "end_date": end_date_str,
                    "calculation_method": "Course hasn't started yet",
                    "payment_type": payment_type,
                    "price_details": price_details
                }
                return result
            
            # Calculate total months
            total_months = self.calculate_months_between_dates(start_date, end_date_str)
            
            # Get end of first month
            end_of_first_month = self.get_end_of_month(start_date_dt)
            
            # For student payments, we need to calculate meetings based on all their groups
            student_groups = student.get("groups", [])
            if not student_groups:
                return {
                    "success": False,
                    "error": "Student is not enrolled in any groups"
                }
            
            # Use the first group for meeting calculations (assuming similar schedule)
            # In the future, you might want to handle multiple groups differently
            first_group_id = self.get_group_id_by_name(student_groups[0])
            if not first_group_id:
                return {
                    "success": False,
                    "error": f"Group '{student_groups[0]}' not found"
                }
            
            # Handle case where we're still in the first month
            if total_months == 0:
                # Count meetings from start date to end date (current month end)
                current_month_meetings = self.count_meetings_in_date_range(
                    first_group_id, start_date_dt, end_of_current_month
                )
                first_month_payment = self.calculate_first_month_payment(monthly_price, current_month_meetings)
                
                return self._create_payment_result(
                    student, monthly_price, 1, current_month_meetings, 
                    first_month_payment, 0, 0, start_date, end_date_str, 
                    payment_type, current_date_str, price_details
                )
            
            # Count meetings in first month only
            first_month_meetings = self.count_meetings_in_date_range(
                first_group_id, start_date_dt, end_of_first_month
            )
            
            # Calculate first month payment
            first_month_payment = self.calculate_first_month_payment(monthly_price, first_month_meetings)
            
            # Calculate remaining months payment (all complete months after first month)
            remaining_months = total_months
            total_months_display = total_months + 1  # +1 because we include first month
            remaining_months_payment = remaining_months * monthly_price
            
            return self._create_payment_result(
                student, monthly_price, total_months_display, first_month_meetings,
                first_month_payment, remaining_months, remaining_months_payment,
                start_date, end_date_str, payment_type, current_date_str, price_details
            )
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error calculating student payment until now: {str(e)}"
            }
    
    def calculate_student_payment_for_period(self, student_id, start_date, end_date):
        """
        Calculate payment for student for a specific period
        Uses student's discounted monthly price based on number of groups and sister discount
        
        Args:
            student_id (str): ID of the student
            start_date (str): Start date when student joined in format "dd/mm/yyyy"
            end_date (str): End date in format "dd/mm/yyyy"
            
        Returns:
            dict: Payment calculation details for the specified period
        """
        try:
            # Get and validate student
            student, validation_result = self._get_student_and_validate(student_id)
            if not student:
                return validation_result
            
            monthly_price = validation_result["monthly_price"]
            price_details = validation_result["price_details"]
            
            # Convert start_date to datetime
            if isinstance(start_date, str):
                start_date_dt = datetime.strptime(start_date, "%d/%m/%Y")
            else:
                start_date_dt = start_date
            
            payment_type = "Full period payment"
            
            # Calculate total months
            total_months = self.calculate_months_between_dates(start_date, end_date)
            
            # Get end of first month
            end_of_first_month = self.get_end_of_month(start_date_dt)
            
            # Get student's groups for meeting calculations
            student_groups = student.get("groups", [])
            if not student_groups:
                return {
                    "success": False,
                    "error": "Student is not enrolled in any groups"
                }
            
            # Use the first group for meeting calculations
            first_group_id = self.get_group_id_by_name(student_groups[0])
            if not first_group_id:
                return {
                    "success": False,
                    "error": f"Group '{student_groups[0]}' not found"
                }
            
            # Handle case where period is within the first month
            if total_months == 0:
                # Count meetings from start date to end date
                end_date_dt = datetime.strptime(end_date, "%d/%m/%Y")
                period_meetings = self.count_meetings_in_date_range(
                    first_group_id, start_date_dt, end_date_dt
                )
                first_month_payment = self.calculate_first_month_payment(monthly_price, period_meetings)
                
                return self._create_payment_result(
                    student, monthly_price, 1, period_meetings, 
                    first_month_payment, 0, 0, start_date, end_date, 
                    payment_type, None, price_details
                )
            
            # Count meetings in first month only
            first_month_meetings = self.count_meetings_in_date_range(
                first_group_id, start_date_dt, end_of_first_month
            )
            
            # Calculate first month payment
            first_month_payment = self.calculate_first_month_payment(monthly_price, first_month_meetings)
            
            # Calculate remaining months payment correctly
            remaining_months = total_months
            remaining_months_payment = remaining_months * monthly_price
            
            # Total months to display = first month + remaining months
            total_months_display = total_months + 1
            
            return self._create_payment_result(
                student, monthly_price, total_months_display, first_month_meetings,
                first_month_payment, remaining_months, remaining_months_payment,
                start_date, end_date, payment_type, None, price_details
            )
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error calculating student payment for period: {str(e)}"
            }
    
    def calculate_payment_until_now(self, group_id, start_date):
        """
        Calculate payment from start date until end of current month (legacy method for groups)
        
        Args:
            group_id (str): ID of the group/course
            start_date (str): Start date when student joined in format "dd/mm/yyyy"
            
        Returns:
            dict: Payment calculation details until current month end
        """
        try:
            # Get and validate group
            group, validation_result = self._get_group_and_validate(group_id)
            if not group:
                return validation_result
            
            monthly_price = validation_result["monthly_price"]
            
            # Convert start_date to datetime
            if isinstance(start_date, str):
                start_date_dt = datetime.strptime(start_date, "%d/%m/%Y")
            else:
                start_date_dt = start_date
            
            # Use end of current month
            current_date = datetime.now()
            end_of_current_month = self.get_end_of_month(current_date)
            end_date_str = end_of_current_month.strftime("%d/%m/%Y")
            payment_type = "Until current month end"
            current_date_str = current_date.strftime("%d/%m/%Y")
            
            # If start date is after current date, no payment needed yet
            if start_date_dt > current_date:
                return {
                    "success": True,
                    "entity_name": group.get("name", ""),
                    "entity_type": "group",
                    "monthly_price": monthly_price,
                    "total_months": 0,
                    "first_month_meetings": 0,
                    "first_month_payment": 0,
                    "remaining_months": 0,
                    "remaining_months_payment": 0,
                    "total_payment": 0,
                    "start_date": start_date,
                    "current_date": current_date_str,
                    "end_date": end_date_str,
                    "calculation_method": "Course hasn't started yet",
                    "payment_type": payment_type
                }
            
            # Calculate total months
            total_months = self.calculate_months_between_dates(start_date, end_date_str)
            
            # Get end of first month
            end_of_first_month = self.get_end_of_month(start_date_dt)
            
            # Handle case where we're still in the first month
            if total_months == 0:
                # Count meetings from start date to end date (current month end)
                current_month_meetings = self.count_meetings_in_date_range(
                    group_id, start_date_dt, end_of_current_month
                )
                first_month_payment = self.calculate_first_month_payment(monthly_price, current_month_meetings)
                
                return self._create_payment_result(
                    group, monthly_price, 1, current_month_meetings, 
                    first_month_payment, 0, 0, start_date, end_date_str, 
                    payment_type, current_date_str
                )
            
            # Count meetings in first month only
            first_month_meetings = self.count_meetings_in_date_range(
                group_id, start_date_dt, end_of_first_month
            )
            
            # Calculate first month payment
            first_month_payment = self.calculate_first_month_payment(monthly_price, first_month_meetings)
            
            # Calculate remaining months payment (all complete months after first month)
            remaining_months = total_months
            total_months_display = total_months + 1  # +1 because we include first month
            remaining_months_payment = remaining_months * monthly_price
            
            return self._create_payment_result(
                group, monthly_price, total_months_display, first_month_meetings,
                first_month_payment, remaining_months, remaining_months_payment,
                start_date, end_date_str, payment_type, current_date_str
            )
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error calculating payment until now: {str(e)}"
            }
    
    def calculate_payment_for_period(self, group_id, start_date, end_date):
        """
        Calculate payment for a specific period (legacy method for groups)
        
        Args:
            group_id (str): ID of the group/course
            start_date (str): Start date when student joined in format "dd/mm/yyyy"
            end_date (str): End date in format "dd/mm/yyyy"
            
        Returns:
            dict: Payment calculation details for the specified period
        """
        try:
            # Get and validate group
            group, validation_result = self._get_group_and_validate(group_id)
            if not group:
                return validation_result
            
            monthly_price = validation_result["monthly_price"]
            
            # Convert start_date to datetime
            if isinstance(start_date, str):
                start_date_dt = datetime.strptime(start_date, "%d/%m/%Y")
            else:
                start_date_dt = start_date
            
            payment_type = "Full period payment"
            
            # Calculate total months
            total_months = self.calculate_months_between_dates(start_date, end_date)
            
            # Get end of first month
            end_of_first_month = self.get_end_of_month(start_date_dt)
            
            # Handle case where period is within the first month
            if total_months == 0:
                # Count meetings from start date to end date
                end_date_dt = datetime.strptime(end_date, "%d/%m/%Y")
                period_meetings = self.count_meetings_in_date_range(
                    group_id, start_date_dt, end_date_dt
                )
                first_month_payment = self.calculate_first_month_payment(monthly_price, period_meetings)
                
                return self._create_payment_result(
                    group, monthly_price, 1, period_meetings, 
                    first_month_payment, 0, 0, start_date, end_date, 
                    payment_type
                )
            
            # Count meetings in first month only
            first_month_meetings = self.count_meetings_in_date_range(
                group_id, start_date_dt, end_of_first_month
            )
            
            # Calculate first month payment
            first_month_payment = self.calculate_first_month_payment(monthly_price, first_month_meetings)
            
            # Calculate remaining months payment correctly
            remaining_months = total_months
            remaining_months_payment = remaining_months * monthly_price
            
            # Total months to display = first month + remaining months
            total_months_display = total_months + 1
            
            return self._create_payment_result(
                group, monthly_price, total_months_display, first_month_meetings,
                first_month_payment, remaining_months, remaining_months_payment,
                start_date, end_date, payment_type
            )
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error calculating payment for period: {str(e)}"
            }
    
    def get_student_payment_amount_until_now(self, student_id, start_date):
        """
        Returns only the total payment amount for student until current month end
        
        Args:
            student_id (str): ID of the student
            start_date (str): Start date when student joined in format "dd/mm/yyyy"
            
        Returns:
            float: Total payment amount, or 0 if error
        """
        result = self.calculate_student_payment_until_now(student_id, start_date)
        if result.get("success"):
            return result["total_payment"]
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
            return 0
    
    def get_student_payment_amount_for_period(self, student_id, start_date, end_date):
        """
        Returns only the total payment amount for student for a specific period
        
        Args:
            student_id (str): ID of the student
            start_date (str): Start date when student joined in format "dd/mm/yyyy"
            end_date (str): End date in format "dd/mm/yyyy"
            
        Returns:
            float: Total payment amount, or 0 if error
        """
        result = self.calculate_student_payment_for_period(student_id, start_date, end_date)
        if result.get("success"):
            return result["total_payment"]
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
            return 0
    
    def get_payment_amount_until_now(self, group_id, start_date):
        """
        Returns only the total payment amount until current month end (legacy method for groups)
        
        Args:
            group_id (str): ID of the group/course
            start_date (str): Start date when student joined in format "dd/mm/yyyy"
            
        Returns:
            float: Total payment amount, or 0 if error
        """
        result = self.calculate_payment_until_now(group_id, start_date)
        if result.get("success"):
            return result["total_payment"]
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
            return 0
    
    def get_payment_amount_for_period(self, group_id, start_date, end_date):
        """
        Returns only the total payment amount for a specific period (legacy method for groups)
        
        Args:
            group_id (str): ID of the group/course
            start_date (str): Start date when student joined in format "dd/mm/yyyy"
            end_date (str): End date in format "dd/mm/yyyy"
            
        Returns:
            float: Total payment amount, or 0 if error
        """
        result = self.calculate_payment_for_period(group_id, start_date, end_date)
        if result.get("success"):
            return result["total_payment"]
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
            return 0

    def calculate_payment(self, group_id, start_date, end_date=None):
        """
        Calculate payment for student based on course duration (legacy method for groups)
        If end_date is None, calculates until end of current month
        
        Args:
            group_id (str): ID of the group/course
            start_date (str): Start date when student joined in format "dd/mm/yyyy"
            end_date (str, optional): End date in format "dd/mm/yyyy". If None, uses current month end.
            
        Returns:
            dict: Payment calculation details
        """
        if end_date is None:
            return self.calculate_payment_until_now(group_id, start_date)
        else:
            return self.calculate_payment_for_period(group_id, start_date, end_date)
    
    def calculate_student_payment(self, student_id, start_date, end_date=None):
        """
        Calculate payment for student based on course duration with all discounts applied
        If end_date is None, calculates until end of current month
        
        Args:
            student_id (str): ID of the student
            start_date (str): Start date when student joined in format "dd/mm/yyyy"
            end_date (str, optional): End date in format "dd/mm/yyyy". If None, uses current month end.
            
        Returns:
            dict: Payment calculation details with discount information
        """
        if end_date is None:
            return self.calculate_student_payment_until_now(student_id, start_date)
        else:
            return self.calculate_student_payment_for_period(student_id, start_date, end_date)
    
    def get_all_students_payment_summary(self):
        """
        Get payment summary for all students with their current monthly prices
        
        Returns:
            list: List of student payment summaries
        """
        try:
            students = self.load_students()
            summary = []
            
            for student in students:
                student_id = student.get("id")
                if not student_id:
                    continue
                
                price_calc = self.calculate_monthly_price_with_discounts(student_id)
                if price_calc.get("success"):
                    summary.append({
                        "student_id": student_id,
                        "student_name": student.get("name", ""),
                        "groups": student.get("groups", []),
                        "has_sister": student.get("has_sister", False),
                        "join_date": student.get("join_date", ""),
                        "payment_status": student.get("payment_status", ""),
                        "monthly_price": price_calc["final_monthly_price"],
                        "num_groups": price_calc["num_groups"],
                        "total_discount": price_calc["total_discount"],
                        "price_breakdown": {
                            "base_price_per_group": price_calc["base_price"],
                            "price_before_discounts": price_calc["price_before_discounts"],
                            "groups_discount": price_calc["price_before_discounts"] - price_calc["price_after_groups_discount"],
                            "sister_discount": price_calc["sister_discount"],
                            "final_price": price_calc["final_monthly_price"]
                        }
                    })
            
            return summary
            
        except Exception as e:
            print(f"Error getting students payment summary: {e}")
            return []
    
    def update_student_groups(self, student_id, new_groups):
        """
        Update student's groups and recalculate their monthly price
        
        Args:
            student_id (str): ID of the student
            new_groups (list): List of new group names
            
        Returns:
            dict: Updated price calculation
        """
        try:
            students = self.load_students()
            student_found = False
            
            for student in students:
                if student.get("id") == student_id:
                    student["groups"] = new_groups
                    student_found = True
                    break
            
            if not student_found:
                return {
                    "success": False,
                    "error": f"Student with ID {student_id} not found"
                }
            
            # Save updated students data
            with open(self.students_file_path, "w", encoding="utf-8") as f:
                json.dump({"students": students}, f, ensure_ascii=False, indent=2)
            
            # Return new price calculation
            return self.calculate_monthly_price_with_discounts(student_id)
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error updating student groups: {str(e)}"
            }
    
    def update_student_sister_status(self, student_id, has_sister):
        """
        Update student's sister status and recalculate their monthly price
        
        Args:
            student_id (str): ID of the student
            has_sister (bool): Whether student has a sister
            
        Returns:
            dict: Updated price calculation
        """
        try:
            students = self.load_students()
            student_found = False
            
            for student in students:
                if student.get("id") == student_id:
                    student["has_sister"] = has_sister
                    student_found = True
                    break
            
            if not student_found:
                return {
                    "success": False,
                    "error": f"Student with ID {student_id} not found"
                }
            
            # Save updated students data
            with open(self.students_file_path, "w", encoding="utf-8") as f:
                json.dump({"students": students}, f, ensure_ascii=False, indent=2)
            
            # Return new price calculation
            return self.calculate_monthly_price_with_discounts(student_id)
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error updating student sister status: {str(e)}"
            }

    def get_student_payment_explanation(self, student_id, start_date, end_date=None):
        """
        Get detailed explanation of student payment calculation
        
        Args:
            student_id (str): ID of the student
            start_date (str): Start date when student joined in format "dd/mm/yyyy"
            end_date (str, optional): End date in format "dd/mm/yyyy". If None, uses current month end.
            
        Returns:
            dict: Detailed payment explanation
        """
        try:
            # Get student details
            student = self.get_student_by_id(student_id)
            if not student:
                return {
                    "success": False,
                    "error": f"תלמידה עם מזהה {student_id} לא נמצאה"
                }
            
            # Calculate payment details
            if end_date is None:
                payment_result = self.calculate_student_payment_until_now(student_id, start_date)
                calculation_period = "עד סוף החודש הנוכחי"
            else:
                payment_result = self.calculate_student_payment_for_period(student_id, start_date, end_date)
                calculation_period = f"מ-{start_date} עד {end_date}"
            
            if not payment_result.get("success"):
                return payment_result
            
            # Get price calculation details
            price_details = payment_result.get("price_details", {})
            
            # Calculate total paid so far
            payments = student.get('payments', [])
            total_paid = 0
            payment_details = []
            
            for payment in payments:
                try:
                    amount = payment.get('amount', 0)
                    if isinstance(amount, str):
                        amount = float(amount) if amount.strip() else 0
                    elif isinstance(amount, (int, float)):
                        amount = float(amount)
                    else:
                        amount = 0
                    
                    if amount > 0:
                        total_paid += amount
                        payment_details.append({
                            "amount": amount,
                            "date": payment.get('date', ''),
                            "method": payment.get('payment_method', '')
                        })
                except (ValueError, AttributeError):
                    continue
            
            # Create explanation
            explanation = {
                "success": True,
                "student_name": student.get("name", ""),
                "student_id": student_id,
                "calculation_period": calculation_period,
                "join_date": start_date,
                
                # Basic info
                "groups": student.get("groups", []),
                "num_groups": len(student.get("groups", [])),
                "has_sister": student.get("has_sister", False),
                
                # Price calculation breakdown
                "price_breakdown": {
                    "base_price_per_group": price_details.get("base_price", 180),
                    "total_before_discounts": price_details.get("price_before_discounts", 0),
                    "groups_discount": price_details.get("price_before_discounts", 0) - price_details.get("price_after_groups_discount", 0),
                    "sister_discount": price_details.get("sister_discount", 0),
                    "final_monthly_price": price_details.get("final_monthly_price", 0)
                },
                
                # Time calculation
                "time_calculation": {
                    "total_months": payment_result.get("total_months", 0),
                    "first_month_meetings": payment_result.get("first_month_meetings", 0),
                    "first_month_full_price": payment_result.get("first_month_full_price", False),
                    "remaining_months": payment_result.get("remaining_months", 0)
                },
                
                # Payment breakdown
                "payment_breakdown": {
                    "first_month_payment": payment_result.get("first_month_payment", 0),
                    "remaining_months_payment": payment_result.get("remaining_months_payment", 0),
                    "total_required": payment_result.get("total_payment", 0)
                },
                
                # Actual payments
                "payments_made": {
                    "total_paid": total_paid,
                    "payment_details": payment_details,
                    "balance": payment_result.get("total_payment", 0) - total_paid
                }
            }
            
            # Add summary - עם try/catch כדי לראות מה השגיאה
            try:
                print("DEBUG: Creating payment summary...")
                explanation["summary"] = self._create_payment_summary(explanation)
                print(f"DEBUG: Summary created, length: {len(explanation['summary']) if explanation['summary'] else 0}")
            except Exception as summary_error:
                print(f"DEBUG: Error creating summary: {summary_error}")
                import traceback
                traceback.print_exc()
                explanation["summary"] = f"שגיאה ביצירת הסיכום: {str(summary_error)}"
            
            return explanation
            
        except Exception as e:
            print(f"DEBUG: Error in get_student_payment_explanation: {e}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "error": f"שגיאה בחישוב הסבר התשלום: {str(e)}"
            }

    def _create_payment_summary(self, explanation):
        """Create a detailed payment summary explanation"""
        try:
            # Extract all needed data from explanation object
            student_name = explanation.get("student_name", "")
            groups = explanation.get("groups", [])
            has_sister = explanation.get("has_sister", False)
            join_date = explanation.get("join_date", "")
            period = explanation.get("calculation_period", "")
            student_id = explanation.get("student_id", "")
            
            # Price data
            price_breakdown = explanation.get("price_breakdown", {})
            base_price = price_breakdown.get("base_price_per_group", 180)
            num_groups = explanation.get("num_groups", 0)
            final_monthly_price = price_breakdown.get("final_monthly_price", 0)
            groups_discount = price_breakdown.get("groups_discount", 0)
            sister_discount = price_breakdown.get("sister_discount", 0)
            
            # Time data
            time_calc = explanation.get("time_calculation", {})
            total_months = time_calc.get("total_months", 0)
            first_month_meetings = time_calc.get("first_month_meetings", 0)
            first_month_full_price = time_calc.get("first_month_full_price", False)
            remaining_months = time_calc.get("remaining_months", 0)
            
            # Payment data
            payment_breakdown = explanation.get("payment_breakdown", {})
            first_month_payment = payment_breakdown.get("first_month_payment", 0)
            remaining_months_payment = payment_breakdown.get("remaining_months_payment", 0)
            total_required = payment_breakdown.get("total_required", 0)
            
            # Payments made
            payments_made = explanation.get("payments_made", {})
            total_paid = payments_made.get("total_paid", 0)
            balance = payments_made.get("balance", 0)
            
            # חישוב תשלום לכל הקורס (אם יש מידע על תאריך סיום)
            total_course_payment = 0
            course_end_info = ""
            
            try:
                # נמצא את תאריך הסיום המאוחר ביותר מכל הקבוצות
                latest_end_date = ""
                for group_name in groups:
                    group_id = self.get_group_id_by_name(group_name)
                    if group_id:
                        group = self.get_group_by_id(group_id)
                        if group:
                            group_end_date = group.get("group_end_date", "")
                            if group_end_date > latest_end_date:
                                latest_end_date = group_end_date
                
                if latest_end_date and student_id:
                    total_course_payment = self.get_student_payment_amount_for_period(
                        student_id, join_date, latest_end_date
                    )
                    course_end_info = f" (עד {latest_end_date})"
            except Exception as e:
                print(f"DEBUG: Error calculating total course payment: {e}")
            
            # יצירת סיכום מפורט
            summary_lines = [
                f"📊 חישוב תשלום מפורט עבור {student_name}",
                f"📅 תקופת החישוב: {period}",
                f"📅 תאריך הצטרפות: {join_date}",
                "",
                "=" * 40,
                "💰 חישוב מחיר חודשי:",
                "=" * 40,
                f"🎭 קבוצות: {', '.join(groups)} ({num_groups} קבוצות)",
                f"💵 מחיר בסיס: {base_price * num_groups}₪ ({base_price}₪ × {num_groups})",
            ]
            
            # הנחות
            if groups_discount > 0:
                summary_lines.append(f"🎯 הנחת קבוצות מרובות: -{groups_discount}₪")
            if sister_discount > 0:
                summary_lines.append(f"👭 הנחת אחיות: -{sister_discount}₪")
            
            summary_lines.append(f"🎯 מחיר חודשי סופי: {final_monthly_price}₪")
            
            # פירוט תקופת התשלום
            summary_lines.extend([
                "",
                "=" * 40,
                "📅 פירוט תקופת התשלום:",
                "=" * 40,
            ])
            
            if total_months == 0:
                # רק חודש חלקי
                summary_lines.append("📊 סוג תקופה: חודש חלקי")
                summary_lines.append(f"🗓️ מספר מפגשים: {first_month_meetings}")
                
                if first_month_meetings < 3:
                    summary_lines.append("📐 חישוב: תשלום יחסי (פחות מ-3 מפגשים)")
                    summary_lines.append(f"🧮 {final_monthly_price}₪ ÷ 4 × {first_month_meetings} = {first_month_payment}₪")
                else:
                    summary_lines.append("📐 חישוב: תשלום מלא (3+ מפגשים)")
                    summary_lines.append(f"🧮 {final_monthly_price}₪ (מחיר חודשי מלא)")
            else:
                # חודש ראשון + חודשים נוספים
                summary_lines.append("📊 סוג תקופה: חודש ראשון חלקי + חודשים מלאים")
                summary_lines.append("")
                summary_lines.append("🗓️ החודש הראשון:")
                summary_lines.append(f"   📅 מספר מפגשים: {first_month_meetings}")
                
                if first_month_meetings < 3:
                    summary_lines.append("   📐 חישוב: תשלום יחסי (פחות מ-3 מפגשים)")
                    summary_lines.append(f"   🧮 {final_monthly_price}₪ ÷ 4 × {first_month_meetings} = {first_month_payment}₪")
                    summary_lines.append("   💡 הסבר: מחלקים את המחיר ב-4 וכופלים במספר המפגשים")
                else:
                    summary_lines.append("   📐 חישוב: תשלום מלא (3+ מפגשים)")
                    summary_lines.append(f"   🧮 {final_monthly_price}₪ (מחיר חודשי מלא)")
                    summary_lines.append("   💡 הסבר: 3+ מפגשים = מחיר חודשי מלא")
                
                if remaining_months > 0:
                    summary_lines.append("")
                    summary_lines.append("🗓️ חודשים נוספים:")
                    summary_lines.append(f"   📊 מספר חודשים מלאים: {remaining_months}")
                    summary_lines.append(f"   🧮 {final_monthly_price}₪ × {remaining_months} = {remaining_months_payment}₪")
            
            # סיכום התשלום
            summary_lines.extend([
                "",
                "=" * 40,
                "💳 סיכום התשלום:",
                "=" * 40,
            ])
            
            if total_months == 0:
                summary_lines.append(f"💰 תשלום לתקופה: {first_month_payment}₪")
            else:
                summary_lines.append("💰 פירוט:")
                summary_lines.append(f"   🗓️ חודש ראשון: {first_month_payment}₪")
                if remaining_months_payment > 0:
                    summary_lines.append(f"   🗓️ חודשים נוספים: {remaining_months_payment}₪")
            
            summary_lines.append(f"🎯 סה\"כ נדרש עד כה: {total_required}₪")
            
            # הוספת מידע על כל הקורס אם זמין
            if total_course_payment > 0:
                summary_lines.append(f"🎯 סה\"כ לכל הקורס{course_end_info}: {total_course_payment}₪")
            
            # מצב תשלומים משופר
            summary_lines.extend([
                "",
                "=" * 40,
                "💰 מצב תשלומים נוכחי:",
                "=" * 40,
                f"💵 שולם עד כה: {total_paid}₪",
            ])
            
            if balance > 0:
                # יש חוב
                summary_lines.append(f"❌ יתרת חוב עד כה: {balance}₪")
                percentage_paid = (total_paid / total_required * 100) if total_required > 0 else 0
                summary_lines.append(f"📈 אחוז ששולם עד כה: {percentage_paid:.1f}%")
            elif balance == 0:
                # שולם במלואו עד כה
                summary_lines.append("✅ סטטוס עד כה: שולם במלואו")
                
                # בדיקה אם יש עוד תשלומים עד סוף הקורס
                if total_course_payment > total_required:
                    remaining_for_course = total_course_payment - total_paid
                    if remaining_for_course > 0:
                        summary_lines.append(f"📋 נותר לשלם עד סוף הקורס: {remaining_for_course}₪")
                    else:
                        summary_lines.append("🎉 שולם גם לכל הקורס!")
                else:
                    summary_lines.append("🎉 מעולה! התשלום מושלם")
            else:
                # שילם יותר מהנדרש עד כה
                overpaid_amount = abs(balance)
                summary_lines.append(f"💰 שילם יותר מהנדרש עד כה: +{overpaid_amount}₪")
                
                if total_course_payment > 0:
                    # בדיקה אם שילם יותר מכל הקורס
                    total_course_balance = total_course_payment - total_paid
                    
                    if total_course_balance > 0:
                        summary_lines.append(f"📋 נותר לשלם עד סוף הקורס: {total_course_balance}₪")
                        summary_lines.append("📊 סטטוס: שילם מראש חלק מהתשלומים הבאים")
                    elif total_course_balance == 0:
                        summary_lines.append("✅ שילם את כל הקורס במלואו!")
                        summary_lines.append("🎉 מעולה! התשלום לכל הקורס מושלם")
                    else:
                        summary_lines.append(f"💰 שילם יתר על כל הקורס: {abs(total_course_balance)}₪")
                        summary_lines.append("📊 ניתן להחזיר את העודף או לזכות לקורס הבא")
                else:
                    summary_lines.append("📊 סטטוס: שילם מראש")
            
            return "\n".join(summary_lines)
            
        except Exception as e:
            print(f"DEBUG: Error in _create_payment_summary: {e}")
            return f"שגיאה ביצירת הסיכום: {str(e)}"
