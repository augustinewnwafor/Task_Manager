from brownie import TodoList, network
from scripts.helpful_scripts import get_account

def main():
    account = get_account()
    todo = TodoList[-1]    # latest deployed contract

    while True:
        print("\n=== Decentralized To-Do List ===")
        print("1. Add task")
        print("2. View all tasks")
        print("3. Mark task completed")
        print("4. Delete task")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            description = input("Enter task description: ")
            tx = todo.addTask(description, {"from": account})
            tx.wait(1)
            print("✅ Task added successfully!")

        elif choice == "2":
            tasks = todo.getAllTasks({"from": account})
            if len(tasks) == 0:
                print("📭 No tasks yet.")
            else:
                for t in tasks:
                    status = "✅ Completed" if t[2] else "❌ Pending"
                    print(f"[{t[0]}] {t[1]} --> {status}")

        elif choice == "3":
            task_id = int(input("Enter task ID to toggle completion: "))
            tx = todo.toggleCompletion(task_id, {"from": account})
            tx.wait(1)
            print(f"🔄 Task {task_id} completion status updated!")

        elif choice == "4":
            task_id = int(input("Enter task ID to delete: "))
            tx = todo.deleteTask(task_id, {"from": account})
            tx.wait(1)
            print(f"🗑️ Task {task_id} deleted!")

        elif choice == "5":
            print("👋 Exiting To-Do List. Goodbye!")
            break

        else:
            print("❌ Invalid choice. Try again.")
