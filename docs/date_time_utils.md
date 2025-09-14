
### docs/date_time_utils.md
```markdown
# Date & Time Utilities

Functions for date and time operations.

## Functions

### `convert_timezone(dt, from_tz, to_tz)`

Convert a datetime from one timezone to another.

**Parameters:**
- `dt` (datetime): The datetime to convert.
- `from_tz` (str): The source timezone.
- `to_tz` (str): The target timezone.

**Returns:**
- datetime: The converted datetime.

**Example:**
```python
from datetime import datetime
from priyam.date_time_utils import convert_timezone

dt = datetime(2023, 1, 1, 12, 0, 0)
result = convert_timezone(dt, 'UTC', 'US/Eastern')
print(result)  # 2023-01-01 07:00:00-05:00

---

`countdown_timer(end_time)`
Calculate the time remaining until a specified end time.

Parameters:
end_time (datetime): The end time to count down to.

Returns:
dict: A dictionary with days, hours, minutes, and seconds remaining.

Example:
`from datetime import datetime, timedelta
from priyam.date_time_utils import countdown_timer

end_time = datetime.now() + timedelta(days=1, hours=2, minutes=30)
result = countdown_timer(end_time)
print(result)  # {'days': 1, 'hours': 2, 'minutes': 30, 'seconds': 0}`

--- 

`working_days_calculator(start_date, end_date, holidays=None)`
Calculate the number of working days between two dates.

Parameters:

start_date (datetime): The start date.

end_date (datetime): The end date.

holidays (list): List of holiday dates to exclude.

Returns:

int: The number of working days.

Example:
`from datetime import datetime
from priyam.date_time_utils import working_days_calculator

start = datetime(2023, 1, 1)
end = datetime(2023, 1, 10)
holidays = [datetime(2023, 1, 2).date()]
result = working_days_calculator(start, end, holidays)
print(result)  # 5`