mock_python_val="""Sure! Below is a simple Python script that demonstrates how to create a basic program to manage a to-do list. The program allows users to add, remove, and view tasks.

```python
class TodoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)
        print(f'Task &quot;{task}&quot; added to the to-do list!')

    def remove_task(self, task):
        if task in self.tasks:
            self.tasks.remove(task)
            print(f'Task &quot;{task}&quot; removed from the to-do list!')
        else:
            print(f'Task &quot;{task}&quot; not found in the to-do list!')

    def view_tasks(self):
        if not self.tasks:
            print(&quot;Your to-do list is empty.&quot;)
        else:
            print(&quot;Your to-do list:&quot;)
            for index, task in enumerate(self.tasks, start=1):
                print(f&quot;{index}. {task}&quot;)

def main():
    todo_list = TodoList()
    
    while True:
        print(&quot;\nOptions:&quot;)
        print(&quot;1. Add task&quot;)
        print(&quot;2. Remove task&quot;)
        print(&quot;3. View tasks&quot;)
        print(&quot;4. Exit&quot;)
        
        choice = input(&quot;Choose an option (1-4): &quot;)

        if choice == '1':
            task = input(&quot;Enter the task to add: &quot;)
            todo_list.add_task(task)
        elif choice == '2':
            task = input(&quot;Enter the task to remove: &quot;)
            todo_list.remove_task(task)
        elif choice == '3':
            todo_list.view_tasks()
        elif choice == '4':
            print(&quot;Exiting the program. Goodbye!&quot;)
            break
        else:
            print(&quot;Invalid choice. Please select a valid option.&quot;)

if __name__ == &quot;__main__&quot;:
    main()
```

### How it Works:
1. **TodoList Class**: Manages the list of tasks with methods to add, remove, and view tasks.
2. **Main Function**: Provides a simple user interface through a command-line menu.
3. **Loop**: Continuously asks for user input until the user chooses to exit.

### Usage:
To use the code:
1. Copy and paste it into a Python environment (like Jupyter Notebook, IDLE, or a simple text editor and run it via the command line).
2. Follow the on-screen prompts to manage your to-do list!

Feel free to modify or expand this code as needed!}"""