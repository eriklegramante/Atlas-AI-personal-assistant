from .system_tools import system_diagnostics
from .math_tools import calculate_basic_math
from .cyber_tools import execute_local_ping

ATLAS_TOOLS = [
    system_diagnostics,
    calculate_basic_math,
    execute_local_ping
    # seu_comando_web
]

TOOLS_MAP = {
    "system_diagnostics": system_diagnostics,
    "calculate_basic_math": calculate_basic_math,
    "execute_local_ling": execute_local_ping 
    # "seu_comando_web": seu_comando_web
}