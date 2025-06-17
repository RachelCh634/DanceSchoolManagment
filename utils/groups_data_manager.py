import json
import os


class GroupsDataManager:
    """Manager for groups data operations"""
    
    def __init__(self):
        self.groups_file = self._get_file_path('groups.json')
    
    def _get_file_path(self, filename):
        """Get absolute path to data file"""
        base_dir = os.path.dirname(os.path.dirname(__file__))
        return os.path.abspath(os.path.join(base_dir, 'data', filename))
    
    def load_groups(self):
        """Load groups from JSON file"""
        try:
            with open(self.groups_file, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"groups": []}

    def save_group(self, group_data):
        """Save new group to file"""
        try:
            data = self.load_groups()
            
            # Generate new ID
            existing_ids = [group.get("id", 0) for group in data.get("groups", [])]
            new_id = max(existing_ids) + 1 if existing_ids else 1
            
            # Create new group
            new_group = {
                "id": new_id,
                "name": group_data["name"],
                "location": group_data["location"],
                "price": group_data["price"],
                "age_group": group_data["age_group"],
                "teacher": group_data["teacher"],
                "students": [],
                "group_start_date": group_data["group_start_date"],
                "day_of_week": group_data["day_of_week"]

            }

            data["groups"].append(new_group)
            
            # Save to file
            with open(self.groups_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return True, "הקבוצה נוספה בהצלחה!"
            
        except Exception as ex:
            return False, f"שגיאה בשמירת הקובץ: {ex}"
    
    def validate_group_data(self, data):
        """Validate group data"""
        required_fields = ["name", "location", "price", "age_group", "teacher"]
        
        for field in required_fields:
            if not data.get(field, "").strip():
                return False, "נא למלא את כל השדות"
        
        return True, ""
