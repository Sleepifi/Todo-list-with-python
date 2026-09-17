import sqlite3
import datetime #для теста
from models import Task,Event
class Database:
    def __init__(self, filename="smart_planner.db"):
        self.filename = filename

    def connect(self):
        return sqlite3.connect(self.filename)

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
        end TEXT NOT NULL
        )
        """)
        connection.commit()
        connection.close()    
    def get_tasks(self):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id,title,priority,duration,status 
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
                deadline=row[4],
                status=row[5]
            )
            tasks.append(task)

        connection.close()
        return tasks
    
    def get_events(self):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id,task_id,start,deadline 
            FROM events
        """)

        rows = cursor.fetchall()
        events = []

        for row in rows:
            event = Event(
                event_id=row[0],
                task_id=row[1],
                start=row[2],
                end=row[3]
            )
            events.append(event)

        connection.close()
        return events
    
    def get_db(self):
        tasks = self.get_tasks()
        events = self.get_events()
        return tasks,events
    def add_task(self, task):
        connection = self.connect()
        cursor = connection.cursor()
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
        connection.close() 
    def add_event(self,event):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO events
            ( task_id, start, end)
            VALUES (?, ?, ?)
        """, (
            event.task_id,
            event.start,
            event.end
        ))

        connection.commit()
        connection.close() 
    
    def update_thing(self,db:str,column:str,value,id:int):
        connection = self.connect()
        cursor = connection.cursor()

        cmd = f"UPDATE {db} SET {column} = ? WHERE id = ?"

        cursor.execute(cmd,(value,id))

        connection.commit()
        connection.close()
    def delete_thing(self,db:str,id:int):
        connection = self.connect()
        cursor = connection.cursor()

        cmd = f"DELETE FROM {db} WHERE id = ?"

        cursor.execute(cmd, (id,))

        connection.commit()
        connection.close()

db = Database("cool.db")
db.create_table()
tta = Task(1,"Test",10,120,"12","good")
print(tta)
eta = Event(1,1,str(datetime.datetime.now()),str(datetime.datetime(2026,9,17)))
#db.add_task(tta)
#db.add_event(eta)
#db.delete_thing("tasks",2)
#db.update_thing("events","start","1111-11-11 11:11:11",1)