class TodoList:
    def __init__(self):
        """
        Initializes a new TodoList instance with an empty list of tasks.
        """
        self.tasks: list = []

    def add_task(self, task: str) -> None:
        """
        Adds a new task to the list.
        :param task: The task to be added.
        """
        self.tasks.append(task)

    def remove_task(self, task: str) -> None:
        """
        Removes a task from the list if it exists.
        :param task: The task to be removed.
        """
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks(self) -> list:
        """
        Returns the list of tasks.
        :return: The list of tasks.
        """
        return self.tasks

    def add_item(self, item: str) -> None:
        """
        Adds an item to the list.
        :param item: The item to be added.
        """
        self.tasks.append(item)

    def remove_item(self, item: str) -> None:
        """
        Removes the first occurrence of an item from the list.
        :param item: The item to be removed.
        """
        if item in self.tasks:
            self.tasks.remove(item)

    def list_items(self) -> list:
        """
        Returns the current list of items.
        :return: The list of items.
        """
        return self.tasks