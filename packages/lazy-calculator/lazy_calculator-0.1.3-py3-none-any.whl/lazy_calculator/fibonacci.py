# Calculate Fibonacci

def fibonacci(n: int, f0: int = 0, f1: int = 1) -> int:
    """Function to calculate fibonacci of a number

    Args:
        n (int): Number to calculate fibonacci

    Returns:
        int: Fibonacci of the number
    """
    if n < 0:
        raise ValueError("Fibonacci of negative number is not defined")

    if n == 0:
        return f0

    if n == 1:
        return f1

    for _ in range(2, n+1):
        f0, f1 = f1, f0+f1

    return f1
