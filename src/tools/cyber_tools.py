import asyncio
from langchain_core.tools import tool
from config.logger import logger


@tool
async def execute_local_ping(host: str) -> str:
    """Executes an asynchronous network ping against a local or remote host.

    Must be triggered whenever the operator asks to verify network connectivity,
    check if an IP address is alive, or test local routing latency.

    Args:
        host (str): The target IP address or domain name to ping (e.g., '127.0.0.1').

    Returns:
        str: A clean, text-to-speech optimized report containing the reachability status.
    """
    logger.info(f"Tool [execute_local_ping] triggered for host: {host}")

    try:
        process = await asyncio.create_subprocess_exec(
            "ping",
            "-c",
            "2",
            host,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            return f"Sir, network connection to {host} is stable. Packets routed successfully."
        else:
            return f"Sir, the target host {host} appears to be unreachable on the local network."

    except Exception as e:
        logger.error(f"Failed to execute local sub-process ping: {e}", exc_info=True)
        return "Sir, I failed to initiate the network subsystem diagnostics due to an internal restriction."
