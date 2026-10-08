import datetime as dt

class Task:
    def __init__(
        self,
        task_id: int,
        title: str,
        priority: int,
        duration: int,
        deadline: dt.datetime,
        status: str,
    ):
        self.task_id = task_id
        self.title = title
        self.priority = priority
        self.duration = duration
        self.deadline = deadline
        self.status = status

    def __str__(self):
        return (
        f"""task_id={self.task_id}
            title={self.title}
            priority={self.priority}
            duration={self.duration}
            deadline={self.deadline}
            status={self.status}
            """
        )

class Event:
    def __init__(
        self,
        event_id: int,
        task_id: int,
        start: dt.datetime,
        end: dt.datetime
    ):
        self.event_id = event_id
        self.task_id = task_id
        self.start = start
        self.end = end

    def __str__(self):
        return(f"""
        event_id={self.event_id}
        task_id={self.task_id}
        start={self.start}
        end={self.end}
        """)
