"""
Helper functions.
"""

import random
import string
from datetime import datetime


def generate_otp(length: int = 6) -> str:
    """تولید کد OTP."""
    return "".join(random.choices(string.digits, k=length))


def generate_order_number() -> str:
    """تولید شماره سفارش."""
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    random_suffix = "".join(random.choices(string.digits, k=6))
    return f"ORD-{timestamp}-{random_suffix}"


def generate_transaction_id() -> str:
    """تولید شناسه تراکنش."""
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    random_suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return f"TXN-{timestamp}-{random_suffix}"
