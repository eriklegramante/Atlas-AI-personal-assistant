from .system_tools import system_diagnostics
from .math_tools import calculate_basic_math
from .cyber_tools import execute_local_ping
from .web_tools import web_search

ATLAS_TOOLS = [
    system_diagnostics,
    calculate_basic_math,
    execute_local_ping,
    web_search,
]

TOOLS_MAP = {
    "system_diagnostics": system_diagnostics,
    "calculate_basic_math": calculate_basic_math,
    "execute_local_ling": execute_local_ping,
    "web_search": web_search,
}
