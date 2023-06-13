from datetime import date
from enum import Enum

class Weekday(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7
    
    @classmethod
    def from_date(cls, date: date):
        return cls(date.isoweekday())
    
print(Weekday.from_date(date.today()))

print(date.today().isoweekday())
