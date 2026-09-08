class Task:
    def __init__(self,name,priority,duration,status):
        self.name = name
        self.priority = priority
        self.duration = duration
        self.status = status

    def __str__(self):
        return(
            f"""
            {self.name}
            Приоритет: {self.priority}
            Время на выполнение: {self.duration}
            Статус: {self.status}
            """
        )
class Storage:
    def __init__(self,FileName):
        self.FileName = FileName

    def load_file(self):
        try:
            with open(self.FileName,"r", encoding="utf-8") as file:
                return [line.strip() for line in file]
        except FileNotFoundError:
            print(f"Ошибка: FileNotFoundError")

    def save_file(self,tasks):
        with open(self.FileName,"w", encoding="utf-8") as file:
            for task in tasks:
                file.write(str(task) + "\n")

class TodoList:
    def __init__(self,tasks=None):
        self.tasks = tasks if tasks is not None else []

    def add_task(self,task):
        if task:
            self.tasks.append(task)
        else:
            print("Задача не может быть пустой")
    def delete_task(self):
        task_id = input("Введите номер задачи")
        if task_id <= 1 or task_id <= len(self.tasks):
            self.tasks.pop(task_id - 1)
    def show_tasks(self):
        """Показывает список задач."""
        if not self.tasks:
            print("\nСписок задач пуст.")
            return

        print("\n--- TODO LIST ---")
        for i, task in enumerate(self.tasks, start=1):
            print(f"{i}. {task}")




def main():
    #НА ЗАВТРА: Заменить .txt на .json
    storage = Storage("todos.txt")

    tasks = storage.load_file()

    todo = TodoList(tasks)

    while True:
        choice = input("Введите вариант ")

        if choice == "2":
            #Запросы к Task
            name = input("Введите имя ")
            priority = input("Введите приоритет от 0 до 10 ")
            duration = input("Дуратион ")
            status = input("Введите статус ")

            task = Task(name,priority,duration,status)
            todo.add_task(task)

            todo.show_tasks()
        if choice == "4":
            storage.save_file(tasks)
            exit()

if __name__ == "__main__":
    main()
