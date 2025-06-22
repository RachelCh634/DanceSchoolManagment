import json
import os
from datetime import datetime, timedelta

class PaymentCalculator:
    def __init__(self):
        self.groups_file_path = "data/groups.json"
    
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
    
    def _get_group_and_validate(self, group_id):
        """Helper method to get group and validate basic requirements"""
        group = self.get_group_by_id(group_id)
        if not group:
            return None, {
                "success": False,
                "error": f"Group with ID {group_id} not found"
            }
        
        monthly_price = float(group.get("price", 0))
        if monthly_price == 0:
            return None, {
                "success": False,
                "error": "Monthly price not found for this group"
            }
        
        return group, {"monthly_price": monthly_price}
    
    def _create_payment_result(self, group, monthly_price, total_months, first_month_meetings, 
                             first_month_payment, remaining_months, remaining_months_payment,
                             start_date, end_date, payment_type, current_date=None):
        """Helper method to create standardized payment result"""
        total_payment = first_month_payment + remaining_months_payment
        
        result = {
            "success": True,
            "group_name": group.get("name", ""),
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
            
        return result
    
    def calculate_payment_until_now(self, group_id, start_date):
        """
        Calculate payment from start date until end of current month
        
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
                    "group_name": group.get("name", ""),
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
        Calculate payment for a specific period
        
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
            
            # 🔧 FIX: Calculate remaining months payment correctly
            # For a full period payment, we need to pay for ALL months
            # total_months already represents the number of complete months after the first month
            remaining_months = total_months  # Don't subtract 1!
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
    
    def get_payment_amount_until_now(self, group_id, start_date):
        """
        Returns only the total payment amount until current month end
        
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
        Returns only the total payment amount for a specific period
        
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
        Calculate payment for student based on course duration
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