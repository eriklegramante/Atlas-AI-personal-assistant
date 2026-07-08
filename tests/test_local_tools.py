import pytest
from src.tools.math_tools import calculate_basic_math
from src.tools.cyber_tools import execute_local_ping

@pytest.mark.asyncio
async def test_calculate_basic_math_success():
    add_result = await calculate_basic_math.ainvoke(
        {"operation": "add", "num1": 10.5, "num2": 4.5}
    )
    assert "evaluates to 15.0" in add_result

    sub_result = await calculate_basic_math.ainvoke(
        {"operation": "subtract", "num1": 20.0, "num2": 5.0}
    )
    assert "results in 15.0" in sub_result

    mul_result = await calculate_basic_math.ainvoke(
        {"operation": "multiply", "num1": 6.0, "num2": 7.0}
    )
    assert "equals 42.0" in mul_result

    div_result = await calculate_basic_math.ainvoke(
        {"operation": "divide", "num1": 100.0, "num2": 4.0}
    )
    assert "yields 25.0" in div_result


@pytest.mark.asyncio
async def test_calculate_basic_math_division_by_zero():
    result = await calculate_basic_math.ainvoke(
        {"operation": "divide", "num1": 50.0, "num2": 0.0}
    )
    assert "Division by zero is undefined" in result


@pytest.mark.asyncio
async def test_execute_local_ping_loopback():
    result = await execute_local_ping.ainvoke({"host": "127.0.0.1"})
    
    assert "network connection to 127.0.0.1 is stable" in result or "unreachable" in result
    assert "Sir" in result