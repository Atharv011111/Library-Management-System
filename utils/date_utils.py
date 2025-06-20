from datetime import datetime

def calculate_late_fee(borrow_date, return_date, free_days=7, fee_per_day=1):
    borrow = datetime.strptime(borrow_date, '%Y-%m-%d')
    return_ = datetime.strptime(return_date, '%Y-%m-%d')
    delta = (return_ - borrow).days - free_days
    return max(0, delta * fee_per_day)