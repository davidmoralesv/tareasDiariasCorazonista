from datetime import date
import holidays

def is_work_day(target_date: date):
    """
    Checks if a given date is a working day in Colombia.
    A working day is a weekday (Monday-Friday) and not a public holiday.

    Args:
        target_date: A datetime.date object.

    Returns:
        True if it's a working day, False otherwise.
    """
    # Get Colombian holidays for the year of the target_date
    co_holidays = holidays.CO(years=target_date.year)

    # target_date.weekday() returns 0 for Monday and 6 for Sunday.
    if target_date.weekday() >= 5:  # Saturday or Sunday
        return False

    # Check if the date is in the list of Colombian holidays.
    if target_date in co_holidays:
        return False

    return True
