# Calculate Factorial

def factorial(n: int) -> int:
    """Function to calculate factorial of a number

    Args:
        n (int): Number to calculate factorial

    Returns:
        int: Factorial of the number
    """
    if n < 0:
        raise ValueError("Factorial of negative number is not defined")

    if n == 0:
        return 1
    else:
        return n * factorial(n-1)
