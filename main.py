# Smart-Personal-Assistant

import heapq
import csv
import os
import json
import webbrowser


# ==================================================
# TASK LIST USING MIN HEAP
# ==================================================

class TaskList:

    def __init__(self):
        self.heap = []
        self.load_tasks()

    def add(self, task, priority=5, note=""):
        heapq.heappush(
            self.heap,
            (priority, task, "Undone", note)
        )
        self.save_tasks()
        print("Task added.")

    def save_tasks(self):
        with open("tasks.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Priority", "Task", "Status", "Note"])
            for priority, task, status, note in self.heap:
                writer.writerow([priority, task, status, note])

    def load_tasks(self):
        if not os.path.exists("tasks.csv"):
            return

        with open("tasks.csv", "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)

            for row in reader:
                if len(row) >= 2:
                    try:
                        priority = int(row[0])
                        task = row[1]
                        status = row[2] if len(row) >= 3 else "Undone"
                        note = row[3] if len(row) >= 4 else ""

                        heapq.heappush(
                            self.heap,
                            (priority, task, status, note)
                        )
                    except ValueError:
                        pass

    def show(self):
        print("\n========== TASK LIST ==========")

        if not self.heap:
            print("No tasks to display.")
            return

        temp_heap = self.heap.copy()
        number = 1

        while temp_heap:
            priority, task, status, note = heapq.heappop(temp_heap)

            print(f"\n{number}. {task}")
            print(f"   Priority: {priority}")
            print(f"   Status: {status}")

            if note.strip():
                print(f"   Note: {note}")

            number += 1

    def select_task(self, action):
        if not self.heap:
            print("No tasks available.")
            return None

        self.show()

        try:
            choice = int(input(f"\nEnter task number to {action}: "))
        except ValueError:
            print("Please enter a valid number.")
            return None

        temp_heap = self.heap.copy()

        for number in range(1, len(temp_heap) + 1):
            item = heapq.heappop(temp_heap)

            if number == choice:
                return item

        print("Invalid task number.")
        return None

    def mark_done(self):
        selected = self.select_task("mark as Done")

        if selected is None:
            return

        priority, task, status, note = selected

        if status == "Done":
            print("This task is already Done.")
            return

        index = self.heap.index(selected)
        self.heap[index] = (priority, task, "Done", note)

        heapq.heapify(self.heap)
        self.save_tasks()
        print("Task marked as Done.")

    def attach_note(self):
        selected = self.select_task("attach a note")

        if selected is None:
            return

        priority, task, status, old_note = selected
        note = input("Enter note: ")

        index = self.heap.index(selected)
        self.heap[index] = (priority, task, status, note)

        heapq.heapify(self.heap)
        self.save_tasks()
        print("Note attached to task.")


# ==================================================
# PERSONAL ASSISTANT
# ==================================================

class Assistant:

    def __init__(self):
        self.task_list = TaskList()
        self.events = []
        self.load_events()

    # ---------------- TASKS ----------------

    def add_task(self, task, note=""):
        self.task_list.add(task, 5, note)

    def add_priority_task(self, task, priority, note=""):
        self.task_list.add(task, priority, note)

    # ---------------- EVENTS ----------------

    def add_event(self, name, date):
        self.events.append((name, date))
        self.save_events()
        print("Event added.")

    def save_events(self):
        with open("events.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Event", "Date"])
            writer.writerows(self.events)

    def load_events(self):
        if not os.path.exists("events.csv"):
            return

        with open("events.csv", "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)

            for row in reader:
                if len(row) >= 2:
                    self.events.append((row[0], row[1]))

    def show_events(self):
        print("\n========== CALENDAR ==========")

        if not self.events:
            print("No events to display.")
            return

        for name, date in self.events:
            print(f"{name} - {date}")

    # ==================================================
    # GRAPHICAL DATA VISUALIZATION
    # ==================================================

    def visualize_data(self):
        tasks = self.task_list.heap

        total = len(tasks)
        done = sum(1 for t in tasks if t[2] == "Done")
        pending = total - done

        priorities = sorted(set(t[0] for t in tasks))
        priority_counts = [
            sum(1 for t in tasks if t[0] == p)
            for p in priorities
        ]

        data = {
            "total": total,
            "done": done,
            "pending": pending,
            "events": len(self.events),
            "priorities": priorities,
            "priority_counts": priority_counts
        }

        html = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Personal Assistant Dashboard</title>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<style>
* { box-sizing: border-box; }

body {
    margin: 0;
    padding: 24px;
    font-family: Arial, sans-serif;
    background: #f1f5f9;
    color: #1e293b;
}

h1 { text-align: center; }

.subtitle {
    text-align: center;
    color: #64748b;
    margin-bottom: 28px;
}

.cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 16px;
    max-width: 1100px;
    margin: auto;
}

.card {
    background: white;
    padding: 22px;
    border-radius: 14px;
    text-align: center;
    box-shadow: 0 3px 12px #00000010;
}

.card h3 {
    color: #64748b;
    font-size: 15px;
}

.number {
    font-size: 34px;
    font-weight: bold;
    margin-top: 12px;
}

.charts {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 20px;
    max-width: 1100px;
    margin: 25px auto;
}

.chart-box {
    background: white;
    padding: 22px;
    border-radius: 14px;
    box-shadow: 0 3px 12px #00000010;
    min-width: 0;
}

.chart-box h2 {
    font-size: 18px;
    text-align: center;
}

.chart-area {
    position: relative;
    height: 300px;
}

footer {
    text-align: center;
    color: #64748b;
    padding: 20px;
}
</style>
</head>

<body>

<h1>Personal Assistant Dashboard</h1>
<p class="subtitle">Task Management and Event Analytics</p>

<div class="cards">
    <div class="card">
        <h3>Total Tasks</h3>
        <div class="number" id="total">0</div>
    </div>
    <div class="card">
        <h3>Completed Tasks</h3>
        <div class="number" id="done">0</div>
    </div>
    <div class="card">
        <h3>Pending Tasks</h3>
        <div class="number" id="pending">0</div>
    </div>
    <div class="card">
        <h3>Calendar Events</h3>
        <div class="number" id="events">0</div>
    </div>
</div>

<div class="charts">
    <div class="chart-box">
        <h2>Task Completion Pie Chart</h2>
        <div class="chart-area">
            <canvas id="pieChart"></canvas>
        </div>
    </div>

    <div class="chart-box">
        <h2>Tasks by Priority</h2>
        <div class="chart-area">
            <canvas id="barChart"></canvas>
        </div>
    </div>

    <div class="chart-box">
        <h2>Completed vs Pending</h2>
        <div class="chart-area">
            <canvas id="statusChart"></canvas>
        </div>
    </div>
</div>

<footer>Personal Assistant | Min Heap and CSV Storage</footer>

<script>
const d = __DATA__;

document.getElementById("total").textContent = d.total;
document.getElementById("done").textContent = d.done;
document.getElementById("pending").textContent = d.pending;
document.getElementById("events").textContent = d.events;

const commonOptions = {
    responsive: true,
    maintainAspectRatio: false
};

new Chart(document.getElementById("pieChart"), {
    type: "pie",
    data: {
        labels: ["Completed", "Pending"],
        datasets: [{
            data: [d.done, d.pending],
            backgroundColor: ["#22c55e", "#f59e0b"]
        }]
    },
    options: commonOptions
});

new Chart(document.getElementById("barChart"), {
    type: "bar",
    data: {
        labels: d.priorities.map(p => "Priority " + p),
        datasets: [{
            label: "Number of Tasks",
            data: d.priority_counts,
            backgroundColor: "#3b82f6"
        }]
    },
    options: {
        ...commonOptions,
        scales: {
            y: {
                beginAtZero: true,
                ticks: { precision: 0 }
            }
        }
    }
});

new Chart(document.getElementById("statusChart"), {
    type: "bar",
    data: {
        labels: ["Tasks"],
        datasets: [
            {
                label: "Completed",
                data: [d.done],
                backgroundColor: "#22c55e"
            },
            {
                label: "Pending",
                data: [d.pending],
                backgroundColor: "#f59e0b"
            }
        ]
    },
    options: {
        ...commonOptions,
        scales: {
            x: { stacked: true },
            y: {
                stacked: true,
                beginAtZero: true,
                ticks: { precision: 0 }
            }
        }
    }
});
</script>

</body>
</html>
"""

        html = html.replace("__DATA__", json.dumps(data))

        filename = os.path.abspath("task_dashboard.html")

        with open(filename, "w", encoding="utf-8") as file:
            file.write(html)

        print("\nDashboard created successfully.")
        print("File location:", filename)
        print("Open task_dashboard.html in a browser to view the charts.")

        try:
            webbrowser.open("file://" + filename)
        except Exception:
            pass

    # ==================================================
    # MAIN MENU
    # ==================================================

    def basic_menu(self):
        while True:
            print("\n========== PERSONAL ASSISTANT ==========")
            print("1. Add Task")
            print("2. Add Task with Priority")
            print("3. Mark Task as Done")
            print("4. Attach Note to Task")
            print("5. Add Event")
            print("6. Show All Tasks and Events")
            print("7. Visualize Data")
            print("8. Exit")

            choice = input("Enter choice: ").strip()

            if choice == "1":
                task = input("Enter task: ")
                note = input("Note (optional): ")
                self.add_task(task, note)

            elif choice == "2":
                task = input("Enter task: ")

                try:
                    priority = int(input("Priority (1 = highest): "))
                    note = input("Note (optional): ")
                    self.add_priority_task(task, priority, note)
                except ValueError:
                    print("Priority must be a number.")

            elif choice == "3":
                self.task_list.mark_done()

            elif choice == "4":
                self.task_list.attach_note()

            elif choice == "5":
                name = input("Enter event name: ")
                date = input("Enter event date: ")
                self.add_event(name, date)

            elif choice == "6":
                self.task_list.show()
                self.show_events()

            elif choice == "7":
                self.visualize_data()

            elif choice == "8":
                print("Exiting Personal Assistant.")
                break

            else:
                print("Invalid choice. Please try again.")


# ==================================================
# RUN PROGRAM
# ==================================================

if __name__ == "__main__":
    assistant = Assistant()
    assistant.basic_menu()
