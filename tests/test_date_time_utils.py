import unittest
from datetime import datetime, timedelta
from priyam.date_time_utils import convert_timezone, countdown_timer, working_days_calculator

class TestDateTimeUtils(unittest.TestCase):
    
    def test_convert_timezone(self):
        dt = datetime(2023, 1, 1, 12, 0, 0)
        converted = convert_timezone(dt, 'UTC', 'US/Eastern')
        self.assertEqual(converted.hour, 7)  # UTC to EST is -5 hours
    
    def test_countdown_timer(self):
        future_time = datetime.now() + timedelta(days=1, hours=2, minutes=30)
        result = countdown_timer(future_time)
        self.assertEqual(result["days"], 1)
        self.assertEqual(result["hours"], 2)
        self.assertEqual(result["minutes"], 30)
    
    def test_working_days_calculator(self):
        start = datetime(2023, 1, 1)  # Sunday
        end = datetime(2023, 1, 10)   # Tuesday
        holidays = [datetime(2023, 1, 2).date()]  # Monday holiday
        
        # 8 days total, minus 2 weekend days, minus 1 holiday = 5 working days
        self.assertEqual(working_days_calculator(start, end, holidays), 5)

if __name__ == "__main__":
    unittest.main()