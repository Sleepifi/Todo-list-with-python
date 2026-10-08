import database
import datetime
from collections import defaultdict
from models import Task,Event


class TodoList:
    def __init__(self, tasks=None, events=None):
        self.tasks = tasks if tasks is not None else []
        self.events = events if events is not None else []
        self.rebuild_index()
 
    def rebuild_index(self):
        self.tasks_by_id = {task.task_id: task for task in self.tasks}
 
        self.events_by_task = defaultdict(list)
        for event in self.events:
            self.events_by_task[event.task_id].append(event)
 
    def get_events_for_task(self, task_id):
        return self.events_by_task.get(task_id, [])
 
    def get_task(self, task_id):
        return {
            "task": self.tasks_by_id.get(task_id).title,
            "events": self.get_events_for_task(task_id),
        }

    def get_tasks_list(self) -> list:
        titles = []

        for task in self.tasks:
            titles.append(task.title)

        return titles

def error_output(text):
        print(f"Ошибка: {text}")
def user_output(text):
        print(f"{text}")
def main():


    db = database.Database()
    db.create_table()

    tasks,events = db.get_db()
    ToDo = TodoList(tasks,events)

    
    while True:
        try:
            choice = input("\nВведите вариант: ")
        except KeyboardInterrupt:
            user_output("До свидания")
            exit()

        if choice == "1":
            tasks_list = ToDo.get_tasks_list()
            print(tasks_list)
        elif choice == "2":
            name = input("Введите имя: ")

            while True:

                priority = input("Введите приоритет от 0 до 10: ")
                if priority.isdigit() and 0 <= int(priority) <= 10:
                    priority = int(priority)
                    break
                error_output("Ввелиие только цифры от 0 до 10")

            while True:

                duration = input("Дуратион: ")
                try:
                    duration = int(duration)
                    break
                except ValueError:
                    error_output("Введите только число")

            while True:

                statuses = ["Done","Working","ToDo"]
                status = input("Введите статус [Done,Working,ToDo]\n:")

                if status in statuses:
                    break
                error_output("Введите только слова [Done,Working,ToDo]")

            task = Task(
                task_id=None,
                title=name,
                priority=priority,
                duration=duration,
                deadline=datetime.datetime(2027,1,1,1,1,1),
                status=status
            )

            db.add_task(task)

        elif choice == "3":
            user_output("Редактирование задачи")
        elif choice == "4":
            while True:

                titd = input("Введите номер задачи для удаления")
                if titd.isdigit():
                    db.delete_thing("tasks",int(titd))
                    break
                error_output("такой задачи нету")

        elif choice == "5":
            break

if __name__ == "__main__":
    main()