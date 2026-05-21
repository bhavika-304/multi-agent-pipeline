import sqlite3
from datetime import datetime


class EpisodicMemory:

    def __init__(self):
        self.db = "memory.db"
        self._create_table()

    def _create_table(self):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS episodes (
                id INTEGER PRIMARY KEY,
                task TEXT,
                agent TEXT,
                success INTEGER,
                result TEXT,
                timestamp TEXT
            )
        """)
        conn.commit()
        conn.close()

    def save(self, task, agent, success, result):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO episodes
            (task, agent, success, result, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (
            task,
            agent,
            1 if success else 0,
            str(result),
            datetime.now().isoformat()
        ))
        conn.commit()
        conn.close()

    def get_similar(self, task):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        words = task.lower().split()
        results = []
        for word in words:
            if len(word) > 4:
                cursor.execute("""
                    SELECT task, agent, success, result
                    FROM episodes
                    WHERE task LIKE ?
                    ORDER BY id DESC
                    LIMIT 3
                """, (f"%{word}%",))
                results.extend(cursor.fetchall())
        conn.close()
        seen = set()
        unique = []
        for r in results:
            if r[0] not in seen:
                seen.add(r[0])
                unique.append(r)
        return unique[:3]

    def as_context(self, task):
        similar = self.get_similar(task)
        if not similar:
            return ""
        lines = ["Similar past tasks:"]
        for past_task, agent, success, result in similar:
            outcome = "succeeded" if success else "failed"
            lines.append(
                f"  - '{past_task[:50]}'"
                f" ran by {agent}"
                f" → {outcome}"
            )
        return "\n".join(lines)