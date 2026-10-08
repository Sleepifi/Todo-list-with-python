import sqlite3
from datetime import datetime

from models import Task, Event


class Database:

    def __init__(self, filename="smart_planner.db"):
        self.filename = filename

    def connect(self):
        connection = sqlite3.connect(self.filename)
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def table_exist(self, name):
        connection = self.connect()
        cursor = connection.cursor()

        result = cursor.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table' AND name = ?
            """,
            (name,)
        ).fetchone()

        connection.close()

        return result is not None

    def create_table(self):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            priority INTEGER NOT NULL,
            duration INTEGER NOT NULL,
            deadline TEXT NOT NULL,
            status TEXT NOT NULL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS events(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER NOT NULL,
            start TEXT NOT NULL,
            end TEXT NOT NULL,
            FOREIGN KEY(task_id) REFERENCES tasks(id) ON DELETE CASCADE
        )
        """)

        connection.commit()
        connection.close()

    def get_tasks(self):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, title, priority, duration, deadline, status
            FROM tasks
        """)

        rows = cursor.fetchall()

        tasks = []

        for row in rows:
            task = Task(
                task_id=row[0],
                title=row[1],
                priority=row[2],
                duration=row[3],
                deadline=datetime.fromisoformat(row[4]),
                status=row[5]
            )

            tasks.append(task)

        connection.close()

        return tasks

    def get_events(self):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, task_id, start, end
            FROM events
        """)

        rows = cursor.fetchall()

        events = []

        for row in rows:
            event = Event(
                event_id=row[0],
                task_id=row[1],
                start=datetime.fromisoformat(row[2]),
                end=datetime.fromisoformat(row[3])
            )

            events.append(event)

        connection.close()

        return events

    def get_db(self):
        tasks = self.get_tasks()
        events = self.get_events()

        return tasks, events

    def add_task(self, task):
        connection = self.connect()
        cursor = connection.cursor()

        try:
            cursor.execute("""
                INSERT INTO tasks
                (title, priority, duration, deadline, status)
                VALUES (?, ?, ?, ?, ?)
            """, (
                task.title,
                task.priority,
                task.duration,
                task.deadline,
                task.status
            ))

            connection.commit()

            task_id = cursor.lastrowid
            task.task_id = task_id

            return task_id

        except sqlite3.IntegrityError:
            connection.rollback()
            print("Не удалось добавить задачу.")
            return None

        finally:
            connection.close()

    def add_event(self, event):
        connection = self.connect()
        cursor = connection.cursor()

        try:
            cursor.execute("""
                INSERT INTO events
                (task_id, start, end)
                VALUES (?, ?, ?)
            """, (
                event.task_id,
                event.start,
                event.end
            ))

            connection.commit()

            event_id = cursor.lastrowid
            event.event_id = event_id

            return event_id

        except sqlite3.IntegrityError:
            connection.rollback()
            print(
                f"Не удалось добавить событие: "
                f"задачи с id {event.task_id} не существует."
            )
            return None

        finally:
            connection.close()

    def update_thing(self, db: str, column: str, value, id: int):
        connection = self.connect()
        cursor = connection.cursor()

        try:
            cmd = f"UPDATE {db} SET {column} = ? WHERE id = ?"
            white_list = {
                "tasks": {"title", "priority", "duration", "deadline", "status"},
                "events": {"task_id", "start", "end"},
            }

            if db not in white_list or column not in white_list[db]:
                raise ValueError("Недопустимая таблица или колонка")
            
            cursor.execute(cmd, (value, id))
            connection.commit()

        except sqlite3.IntegrityError:
            connection.rollback()
            print("Не удалось обновить запись.")

        except ValueError:
            connection.rollback()

        finally:
            connection.close()

    def delete_thing(self, db: str, id: int):
        connection = self.connect()
        cursor = connection.cursor()

        try:
            if db == "tasks":
                cmd = "DELETE FROM tasks WHERE id = ?"
                cursor.execute(cmd, (id,))

            elif db == "events":
                cmd = "DELETE FROM events WHERE id = ?"
                cursor.execute(cmd, (id,))

            connection.commit()

        except sqlite3.IntegrityError:
            connection.rollback()
            print("Не удалось удалить запись.")

        finally:
            connection.close()


if __name__ == "__main__":
    # тест
    db = Database()
    db.create_table()
    """  task = Task(
        1,
        "Test",
        10,
        120,
        "2027-09-17",
        "good"
    ) """
    #task_id = db.add_task(task)
    #print("Создана задача с id:", task_id)
    event = Event(
        1,
        2,
        str(datetime.datetime.now()),
        "2027-09-17 12:00:00"
    )
    event_id = db.add_event(event)
    print("Создано событие с id:", event_id)