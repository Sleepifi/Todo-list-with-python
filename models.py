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
        f""" {self.task_id} = task_id
            {self.title} = title
            {self.priority} = priority
            {self.duration} = duration
            {self.deadline} = deadline
            {self.status} = status
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
