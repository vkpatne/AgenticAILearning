# math_tools.py

def add_numbers(input_str: str) -> str:
    """Add comma-separated numbers: '100, 200, 50' => 350"""
    numbers = [float(x.strip()) for x in input_str.split(",")]
    return str(sum(numbers))

def multiply_numbers(input_str: str) -> str:
    """Multiply two numbers: '5, 20' => 100"""
    a, b = [float(x.strip()) for x in input_str.split(",")]
    return str(a * b)

def calculate_total_cost(input_str: str) -> str:
    """
    Add multiple costs together, input: 'hotel:300, food:150, travel:100'
    """
    try:
        items = input_str.split(",")
        total = sum(float(x.split(":")[1].strip()) for x in items)
        return f"Total cost is {total:.2f}"
    except Exception:
        return "Input format should be like 'hotel:300, food:150, travel:100'"

def calculate_daily_budget(input_str: str) -> str:
    """Calculate daily budget: 'total:1200, days:6' => 200"""
    try:
        parts = dict(part.split(":") for part in input_str.split(","))
        total = float(parts["total"].strip())
        days = int(parts["days"].strip())
        return f"Daily budget is {total / days:.2f}"
    except Exception:
        return "Input format should be like 'total:1200, days:6'"
