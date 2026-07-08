from langchain_core.tools import tool
from config.logger import logger


@tool
async def calculate_basic_math(operation: str, num1: float, num2: float) -> str:
    """Executes basic arithmetic operations (add, subtract, multiply, divide) on two numbers.

    Must be triggered whenever the operator asks for mathematical computations,
    sums, multiplications, or simple accounting tasks via voice.

    Args:
        operation (str): The operational arithmetic type. Must be strictly one of:
            'add', 'subtract', 'multiply', or 'divide'.
        num1 (float): The first numerical parameter.
        num2 (float): The second numerical parameter.

    Returns:
        str: A natural, text-to-speech optimized verbal response stating the exact result.
    """
    logger.info(
        f"Tool [calculate_basic_math] triggered for operational sequence: {operation}"
    )

    try:
        if operation == "add":
            result = num1 + num2
            return f"The sum of {num1} and {num2} evaluates to {result}."

        elif operation == "subtract":
            result = num1 - num2
            return f"Subtracting {num2} from {num1} results in {result}."

        elif operation == "multiply":
            result = num1 * num2
            return f"The multiplication of {num1} by {num2} equals {result}."

        elif operation == "divide":
            if num2 == 0:
                return "Sir, mathematical calculation aborted. Division by zero is undefined."
            result = num1 / num2
            return f"Dividing {num1} by {num2} yields {result}."

        return "Sir, I could not identify a valid operational parameter within the mathematical sequence."

    except Exception as e:
        logger.error(f"Failed to process arithmetic execution loop: {e}", exc_info=True)
        return "Sir, an internal calculation fluctuation occurred while evaluating the numerical data."
