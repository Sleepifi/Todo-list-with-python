import json


class Task:
    def __init__(self, title, priority, duration, status, task_id=None):
        self.id = task_id
        self.title = title
        self.priority = priority
        self.duration = duration
        self.status = status

    def to_json(self):
        return {
            "Id": self.id,
            "Title": self.title,
            "Priority": self.priority,
            "Duration": self.duration,
            "Status": self.status
        }

    def __str__(self):
        return (
            f"\n"
            f"{self.title}\n"
            f"Приоритет: {self.priority}\n"
            f"Время на выполнение: {self.duration}\n"
            f"Статус: {self.status}\n"
        )


class Storage:
    def __init__(self, filename):
        self.filename = filename

    def load_file(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)

                return data.get("Tasks", [])

        except FileNotFoundError:
            print("Файл не найден. Создаю новый.")

            data = {
                "Tasks": []
            }

            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            return []

    def save_file(self, tasks):
        data = {
            "Tasks": tasks
        }

        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4
            )


class TodoList:
    def __init__(self, tasks=None):
        self.tasks = tasks if tasks is not None else []

    def add_task(self, task):
        if task:
            self.tasks.append(task)
        else:
            print("Задача не может быть пустой")

    def delete_task(self):
        try:
            task_id = int(input("Введите номер задачи: "))

            if 1 <= task_id <= len(self.tasks):
                self.tasks.pop(task_id - 1)
            else:
                print("Такой задачи нет.")

        except ValueError:
            print("Введите число.")

    def show_tasks(self):
        if not self.tasks:
            print("\nСписок задач пуст.")
            return

        print("\n--- TODO LIST ---")

        for task in self.tasks:
            print(
                f"{task['Id']}. "
                f"{task['Title']} | "
                f"Приоритет: {task['Priority']} | "
                f"Время: {task['Duration']} | "
                f"Статус: {task['Status']}"
            )


def main():
    storage = Storage("tasks.json")

    tasks = storage.load_file()

    # Восстанавливаем правильные ID
    for i, task in enumerate(tasks, start=1):
        task["Id"] = i

    todo = TodoList(tasks)

    while True:
        choice = input("\nВведите вариант: ")

        if choice == "1":
            todo.show_tasks()

        elif choice == "2":
            name = input("Введите имя: ")
            priority = input("Введите приоритет от 0 до 10: ")
            duration = input("Дуратион: ")
            status = input("Введите статус: ")

            task_id = len(todo.tasks) + 1

            task = Task(
                name,
                priority,
                duration,
                status,
                task_id
            )

            todo.add_task(task.to_json())

            todo.show_tasks()

        elif choice == "4":
            storage.save_file(todo.tasks)
            print("Задачи сохранены.")
            break


if __name__ == "__main__":
    main()
