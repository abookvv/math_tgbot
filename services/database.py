import aiosqlite
import os

DB_PATH = "storage/database.db"

CREATE_TABLES_QUERY = """
CREATE TABLE IF NOT EXISTS quizzes (
    id TEXT PRIMARY KEY,
    title TEXT
);

CREATE TABLE IF NOT EXISTS tickets (
    id TEXT PRIMARY KEY,
    quiz_id TEXT,
    question TEXT,
    answer TEXT,
    FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE
);
"""

class QuizDB:
    def __init__(self, path=DB_PATH):
        self.path = path

    async def get_connection(self):
        return await aiosqlite.connect(self.path)

    async def init(self):
        async with aiosqlite.connect(self.path) as db:
            await db.executescript(CREATE_TABLES_QUERY)
            await db.commit()

    async def add_quiz(self, quiz_id: str, title: str):
        async with aiosqlite.connect(self.path) as db:
            await db.execute("INSERT INTO quizzes (id, title) VALUES (?, ?)", (quiz_id, title))
            await db.commit()

    async def get_quizzes(self):
        async with aiosqlite.connect(self.path) as db:
            async with db.execute("SELECT id, title FROM quizzes") as cursor:
                return await cursor.fetchall()

    async def add_ticket(self, ticket_id: str, quiz_id: str, question: str, answer: str):
        async with aiosqlite.connect(self.path) as db:
            await db.execute("INSERT INTO tickets (id, quiz_id, question, answer) VALUES (?, ?, ?, ?)",
                             (ticket_id, quiz_id, question, answer))
            await db.commit()

    async def get_tickets(self, quiz_id: str):
        async with aiosqlite.connect(self.path) as db:
            async with db.execute("SELECT id, question, answer FROM tickets WHERE quiz_id = ?", (quiz_id,)) as cursor:
                rows = await cursor.fetchall()
                return [
                    {"id": row[0], "question": row[1], "answer": row[2]}
                    for row in rows
                ]

    # посмотрим исправит ли эта функция ошибку
    async def get_ticket_by_id(self, quiz_id: str, ticket_id: str):
        async with aiosqlite.connect(self.path) as db:
            async with db.execute(
                    "SELECT id, question, answer FROM tickets WHERE quiz_id = ? AND id = ?",
                    (quiz_id, ticket_id)
            ) as cursor:
                row = await cursor.fetchone()
                if row:
                    return {
                        "id": row[0],
                        "question": row[1],
                        "answer": row[2]
                    }
                else:
                    return None

    async def delete_quiz_by_id(self, quiz_id: str):
        async with self.get_connection() as db:
            await db.execute("DELETE FROM quizzes WHERE id = ?", (quiz_id,))
            await db.commit()

    async def delete_tickets_by_quiz_id(self, quiz_id: str):
        async with self.get_connection() as db:
            await db.execute("DELETE FROM tickets WHERE quiz_id = ?", (quiz_id,))
            await db.commit()
