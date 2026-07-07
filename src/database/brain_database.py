import json
import aiosqlite
from pathlib import Path
from config.settings import settings
from config.logger import logger


class AtlasBrain:
    """Handles the core storage schema, active conversation streams, and profile tracking layers.

    Leverages non-blocking transactional wrappers via aiosqlite to manage short-term session
    histories alongside key-value persistence arrays representing permanent long-term memory.

    Attributes:
        db_path (Path): Absolute structural destination tracking target database file.
    """

    def __init__(self, db_path: Path = settings.DATABASE_PATH):
        self.db_path = db_path

    async def initialize_db(self) -> None:
        """Asynchronously sets up the runtime database layout and structural index constraints.

        Constructs profiling matrices and rolling message storage rows if they are missing.

        Args:
            None

        Returns:
            None

        Raises:
            Exception: Critical fallback trap propagating SQLite schema errors to the core runtime loop.
        """
        logger.debug(f"Connecting to secure database engine at: {self.db_path}")
        try:
            async with aiosqlite.connect(self.db_path) as conn:
                await conn.execute("""
                    CREATE TABLE IF NOT EXISTS user_profile (
                        key TEXT PRIMARY KEY,
                        value TEXT
                    )
                """)
                await conn.execute("""
                    CREATE TABLE IF NOT EXISTS chat_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id TEXT NOT NULL DEFAULT 'default',
                        role TEXT NOT NULL,
                        content TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                await conn.commit()
            logger.info("ATLAS central database initialized and Git-protected.")
        except Exception as e:
            logger.critical(
                f"Critical failure while initializing database schema: {e}",
                exc_info=True,
            )
            raise e

    async def add_message(
        self, role: str, content: str, session_id: str = "default"
    ) -> None:
        """Appends a single verified interactive message row to the specified session thread.

        Args:
            role (str): Author signature identity mapping the source ('human' or 'ai').
            content (str): Textual body data representing the conversation turn context.
            session_id (str, optional): Target session identity container. Defaults to "default".

        Returns:
            None
        """
        logger.debug(f"Logging record into chat history [{session_id}]: {role}")
        try:
            async with aiosqlite.connect(self.db_path) as conn:
                await conn.execute(
                    "INSERT INTO chat_history (session_id, role, content) VALUES (?, ?, ?)",
                    (session_id, role, content),
                )
                await conn.commit()
        except Exception as e:
            logger.error(f"Failed to commit message record to database: {e}")

    async def get_chat_history(
        self, session_id: str = "default", limit: int = 20
    ) -> list[dict]:
        """Harvests an ordered chronological log segment matching the targeted thread string.

        Pulls latest transactions first based on limits, then inverses the sorting arrays
        to supply structural message timelines to the AI graph.

        Args:
            session_id (str, optional): Target session identity container. Defaults to "default".
            limit (int, optional): Maximum window slice of history items to parse. Defaults to 20.

        Returns:
            list[dict]: Array records displaying 'role' and 'content' metadata keys.
        """
        try:
            async with aiosqlite.connect(self.db_path) as conn:
                query = """
                    SELECT role, content FROM (
                        SELECT id, role, content FROM chat_history 
                        WHERE session_id = ? 
                        ORDER BY id DESC LIMIT ?
                    ) ORDER BY id ASC
                """
                async with conn.execute(query, (session_id, limit)) as cursor:
                    rows = await cursor.fetchall()
                    return [{"role": row[0], "content": row[1]} for row in rows]
        except Exception as e:
            logger.error(
                f"Failed to extract conversation memory context for session {session_id}: {e}"
            )
            return []

    async def clear_session_history(self, session_id: str = "default") -> None:
        """Purges short-term interactive record items bound to a specified session index.

        Args:
            session_id (str, optional): Target session identity container. Defaults to "default".

        Returns:
            None
        """
        logger.warning(
            f"Memory purge protocol activated for runtime session: {session_id}"
        )
        try:
            async with aiosqlite.connect(self.db_path) as conn:
                await conn.execute(
                    "DELETE FROM chat_history WHERE session_id = ?", (session_id,)
                )
                await conn.commit()
            logger.info(
                f"Short-term context for session '{session_id}' completely cleared."
            )
        except Exception as e:
            logger.error(
                f"Error executing memory purge routine for session {session_id}: {e}"
            )

    async def store_fact(self, key: str, value: str) -> None:
        """Overwrites or inserts a profiling parameter item within the vault storage table.

        Args:
            key (str): Unique indexing token descriptor tracking user attributes.
            value (str): Text details allocated to the assigned metadata index key.

        Returns:
            None
        """
        logger.debug(f"Storing profiling fact under key '{key}' into long-term vault.")
        try:
            async with aiosqlite.connect(self.db_path) as conn:
                await conn.execute(
                    "INSERT OR REPLACE INTO user_profile (key, value) VALUES (?, ?)",
                    (key, value),
                )
                await conn.commit()
        except Exception as e:
            logger.error(
                f"Failed to store analytical fact '{key}' in persistence layer: {e}"
            )

    async def get_fact(self, key: str) -> str | None:
        """Queries the persistent profile matrix to match a long-term tracker string.

        Args:
            key (str): Unique tracking item reference key.

        Returns:
            str | None: Retrieved factual value text, or None if the query yields no match.
        """
        try:
            async with aiosqlite.connect(self.db_path) as conn:
                async with conn.execute(
                    "SELECT value FROM user_profile WHERE key = ?", (key,)
                ) as cursor:
                    result = await cursor.fetchone()
                    return result[0] if result else None
        except Exception as e:
            logger.error(
                f"Error accessing user profile metadata vault for key '{key}': {e}"
            )
            return None
