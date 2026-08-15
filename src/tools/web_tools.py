import asyncio
from ddgs import DDGS
from langchain_core.tools import tool
from config.logger import logger
import urllib.parse
import webbrowser


@tool
async def web_search(query: str) -> str:
    """Performs a real-time web search query to retrieve current world facts, news, or live web data.

    Must be triggered whenever the operator asks for real-time information,
    current news, weather updates, external technical documentation, or facts outside local knowledge.

    Args:
        query (str): The search query parameters optimized for search engines.

    Returns:
        str: A clean, text-to-speech optimized verbal summary of the top web search results.
    """
    logger.info(f"Tool [web_search] triggered with query: '{query}'")
    try:
        loop = asyncio.get_event_loop()

        def _fetch_search():
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=3))
                return results

        results = await loop.run_in_executor(None, _fetch_search)

        if not results:
            return (
                f"Sir, my web search for '{query}' returned no relevant live results."
            )

        compiled_snippets = []
        for idx, result in enumerate(results, 1):
            title = result.get("title", "")
            snippet = result.get("body", "")
            compiled_snippets.append(f"Result {idx}: {title} - {snippet}")

        formatted_payload = " ".join(compiled_snippets)
        logger.debug(f"Web search successfully parsed {len(results)} results.")

        return f"Sir, according to real-time web results for '{query}': {formatted_payload}"

    except Exception as e:
        logger.error(f"Failed to execute real-time web search: {e}", exc_info=True)
        return "Sir, I encountered a communication error while attempting to query external web networks."


KNOWN_PLATFORMS = {
    "youtube": "https://www.youtube.com/results?search_query=",
    "facebook": "https://www.facebook.com",
    "instagram": "https://www.instagram.com",
    "github": "https://github.com/search?q=",
    "google": "https://www.google.com/search?q=",
    "linkedin": "https://www.linkedin.com",
}


@tool
async def open_web_resource(target: str, action_query: str = "") -> str:
    """Navigates to web platforms, opens social media, or performs queries on specific sites.

    Must be triggered whenever the operator asks to open a specific website,
    access a platform (like Facebook, YouTube, GitHub), or search/play content on a platform via voice.

    Args:
        target (str): The destination domain or platform identifier (e.g., 'youtube', 'facebook', 'github', 'google').
        action_query (str, optional): The specific query, music name, or search term to execute within that platform. Defaults to "".

    Returns:
        str: A text-to-speech optimized verbal execution status report.
    """
    logger.info(
        f"Tool [open_web_resource] triggered. Target: '{target}', Query: '{action_query}'"
    )
    try:
        target_lower = target.lower().strip()
        encoded_query = urllib.parse.quote(action_query.strip()) if action_query else ""

        if target_lower in KNOWN_PLATFORMS:
            base_url = KNOWN_PLATFORMS[target_lower]

            if action_query and "=" in base_url:
                final_url = f"{base_url}{encoded_query}"
            else:
                final_url = base_url

        elif "." in target_lower:
            final_url = (
                target_lower
                if target_lower.startswith("http")
                else f"https://{target_lower}"
            )

        else:
            final_url = f"https://www.google.com/search?q={urllib.parse.quote(f'{target} {action_query}'.strip())}"

        webbrowser.open(final_url)
        logger.debug(f"Navigated to web resource URL: {final_url}")

        if action_query:
            return f"Sir, I have accessed {target} executing your request for '{action_query}'."
        return f"Sir, I have opened {target} in your default browser."

    except Exception as e:
        logger.error(
            f"Failed to execute web navigation for target '{target}': {e}",
            exc_info=True,
        )
        return "Sir, I encountered a restriction while attempting to launch the requested web resource."
