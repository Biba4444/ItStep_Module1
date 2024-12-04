id_storage = []
notes_storage = []

def file_reader(isID=False):
    def parse_block(block):
        return {
            key.strip(): value.strip()
            for line in block.split("\n")
            if ":" in line
            for key, value in [line.split(":", 1)]
        }

    with open("Notes.txt", "r") as file:
        data = file.read().strip()

    blocks = data.split("\n\n")
    records = [parse_block(block) for block in blocks]

    if isID:
        return [str(record["ID"]) for record in records if "ID" in record]

    return records


notes_storage = file_reader()
id_storage = file_reader(True)

def id_generator() -> int:
    max_numeric_storage = list(map(int, id_storage))
    max_id = max(max_numeric_storage) if max_numeric_storage else 0
    return max_id + 1

def notes_status_creator(task_to_upd: str):
    if task_to_upd == "Priority":    
        new_value_priority = int(input("Enter new priority: 1 - low, 2 - mid, 3 - high: "))
        if new_value_priority in [1, 2, 3]:
            match new_value_priority:
                case 1:
                    return (1, "low")
                case 2:
                    return (2, "mid")
                case 3:
                    return (3, "high")
        else:
            print("Invalid value")
            return False
    elif task_to_upd == "Status":
        new_value_status = int(input("Enter new status: 1 - new, 2 - in-progress, 3 - done: "))
        if new_value_status in [1, 2, 3]:
            match new_value_status:
                case 1:
                    return (1, "new")
                case 2:
                    return (2, "in-progress")
                case 3:
                    return (3, "done")
        else:
            print("Invalid value")
            return False

def notes_creator():    
    task = {}
    note_name = input("Name: ")
    note_description = input("Description: ")
    note_priority = notes_status_creator("Priority")
    if note_priority is False:
        return

    note_status = notes_status_creator("Status")
    if note_status is False:
        return
    note_id = id_generator()
    id_storage.append(note_id)
    task.update({
        "ID": note_id,
        "Name": note_name,
        "Description": note_description,
        "Priority": note_priority,
        "Status": note_status
    })
    notes_storage.append(task)

def file_changer(notes: list):
    with open("Notes.txt", "w") as file:
        for task in notes:
            for key, value in task.items():
                file.write(f"{key}: {value}\n")
            file.write("\n")
            
def notes_status_sorter():
    sorted_status_list = sorted(notes_storage, key=lambda x: x['Status'][0])
    for task in sorted_status_list:
        print(task)
        
def notes_priority_sorter():
    sorted_priority_list = sorted(notes_storage, key=lambda x: x['Priority'][0])
    for task in sorted_priority_list:
        print(task)
        
def notes_remover():
    rem_task_id = str(input("Enter the ID of the task you want to remove: ")).strip()
    task_to_remove = None
    for task in notes_storage:
        if task["ID"] == rem_task_id:
            task_to_remove = task
            break
    if task_to_remove:
        print(f"Found task: {task_to_remove}")
        notes_storage.remove(task_to_remove)
        file_changer(notes_storage)
        print("Task has been succesfully deleted")
            
    
def notes_updater():
    task_id = str(input("Enter the ID of the task you want to update: ")).strip()
    
    task_to_update = None
    for task in notes_storage:
        if task["ID"] == task_id:
            task_to_update = task
            break
    
    if task_to_update:
        print(f"Found task: {task_to_update}")
        
        task_field = int(input("What would you like to update? (1 - Name, 2 - Description, 3 - Priority, 4 - Status): "))
        match task_field:
            case 1:
                new_value = input("Enter new Name: ")
                if new_value:
                    task_to_update["Name"] = new_value
                    file_changer(notes_storage)
            case 2:
                new_value_desc = input("Enter new Description: ")
                if new_value_desc:
                    task_to_update["Description"] = new_value_desc
                    file_changer(notes_storage)
            case 3:
                task_to_update["Priority"] = notes_status_creator("Priority")
                if task_to_update["Priority"] is False:
                    return
                file_changer(notes_storage)
            case 4:
                task_to_update["Status"] = notes_status_creator("Status")
                if task_to_update["Status"] is False:
                    return
                file_changer(notes_storage)
            case _ :
                print("Invalid value")
                return
    
def notes_watcher():
    while True:
        watch_selector = int(input("Type 1 to show your tasklist in default version, 2 to sort by status, 3 to sort by priority, 4 to find by yourself, 0 to return to main menu: "))
        if watch_selector == 0:
            break
        match watch_selector:
            case 1:
                if notes_storage:
                    for task in notes_storage:
                        print(task)
                else:
                    print("No tasks available.")
            case 2:
                if notes_storage:
                    notes_status_sorter()
                else:
                    print("No tasks available to sort by status.")
            case 3:
                if notes_storage:
                    notes_priority_sorter()
                else:
                     print("No tasks available to sort by priority.")
            case 4:
                search_term = input("Enter search term (name or description): ").lower()
                found_tasks = [task for task in notes_storage if search_term in task['Name'].lower() or search_term in task['Description'].lower()]
                if found_tasks:
                    for task in found_tasks:
                        print(task)
            case _ :
                print("Incorrect value")

def start_log():
    while True:
        user_selection = int(input(
            "Type 1 to create a new task, 2 to watch your tasklist, 3 to update tasks, 4 to delete tasks, 0 to leave the program: "
        ))
        match user_selection:
            case 1:
                notes_creator()
                file_changer(notes_storage)
            case 2:
                notes_watcher()
            case 3: 
                notes_updater()
            case 4:
                notes_remover()
            case 0:
                print("Program stopped")
                break
            case _:
                print("Incorrect value, try again please")

start_log()




