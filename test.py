import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime, timedelta

class FlightTestTaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestionnaire de Tâches - Tests en Vol")
        self.root.geometry("1000x600")

        # Types de tâches pour les tests en vol avec codes couleur
        self.task_types = {
            "Préparation du vol": "lightblue",
            "Installation de l'équipement": "lightgreen",
            "Collecte de données": "salmon",
            "Analyse post-vol": "lightgrey"
        }

        # Liste des tâches
        self.tasks = []
        self.scale_factor = 1.0

        # Date d'aujourd'hui
        self.today = datetime.now()

        # Interface graphique
        self.create_widgets()
        self.root.bind("<Configure>", self.resize_widgets)

    def create_widgets(self):
        # Champ d'entrée pour ajouter des tâches
        tk.Label(self.root, text="Nouvelle tâche :").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.task_entry = tk.Entry(self.root, width=40)
        self.task_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Menu déroulant pour choisir le type de tâche
        tk.Label(self.root, text="Type de tâche :").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.task_type = tk.StringVar(self.root)
        self.task_type.set("Préparation du vol")  # Valeur par défaut
        self.task_type_menu = tk.OptionMenu(self.root, self.task_type, *self.task_types.keys())
        self.task_type_menu.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Champ d'entrée pour la date limite
        tk.Label(self.root, text="Date limite (YYYY-MM-DD) :").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.deadline_entry = tk.Entry(self.root, width=15)
        self.deadline_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Champ d'entrée pour la date d'aujourd'hui
        tk.Label(self.root, text="Date d'aujourd'hui (YYYY-MM-DD) :").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.today_entry = tk.Entry(self.root, width=15)
        self.today_entry.insert(0, self.today.strftime("%Y-%m-%d"))  # Valeur par défaut
        self.today_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        # Bouton pour ajouter une tâche
        add_button = tk.Button(self.root, text="Ajouter Tâche", command=self.add_task, width=15)
        add_button.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        # Listboxes pour les tâches "À faire" et "Terminées"
        tk.Label(self.root, text="À faire :").grid(row=4, column=0, padx=10, pady=10)
        self.todo_listbox = tk.Listbox(self.root, width=50, height=15, selectmode=tk.SINGLE)
        self.todo_listbox.grid(row=5, column=0, columnspan=2, padx=10, pady=5)
        self.todo_scrollbar = tk.Scrollbar(self.root, command=self.todo_listbox.yview)
        self.todo_scrollbar.grid(row=5, column=2, sticky="ns")
        self.todo_listbox.config(yscrollcommand=self.todo_scrollbar.set)

        tk.Label(self.root, text="Terminées :").grid(row=4, column=3, padx=10, pady=10)
        self.completed_listbox = tk.Listbox(self.root, width=50, height=15, selectmode=tk.SINGLE)
        self.completed_listbox.grid(row=5, column=3, columnspan=2, padx=10, pady=5)
        self.completed_scrollbar = tk.Scrollbar(self.root, command=self.completed_listbox.yview)
        self.completed_scrollbar.grid(row=5, column=5, sticky="ns")
        self.completed_listbox.config(yscrollcommand=self.completed_scrollbar.set)

        # Boutons pour marquer comme terminée et supprimer
        complete_button = tk.Button(self.root, text="Marquer comme Terminée", command=self.complete_task, width=20)
        complete_button.grid(row=7, column=0, padx=10, pady=10)

        delete_button = tk.Button(self.root, text="Supprimer Tâche", command=self.delete_task, width=20)
        delete_button.grid(row=7, column=1, padx=10, pady=10)

        # Boutons pour filtrer les tâches
        tk.Button(self.root, text="Tâches d'Aujourd'hui", command=lambda: self.filter_tasks('today')).grid(row=8, column=0, padx=10, pady=5)
        tk.Button(self.root, text="Tâches de cette Semaine", command=lambda: self.filter_tasks('week')).grid(row=8, column=1, padx=10, pady=5)
        tk.Button(self.root, text="Tâches de ce Mois", command=lambda: self.filter_tasks('month')).grid(row=8, column=2, padx=10, pady=5)
        tk.Button(self.root, text="Tâches de cette Année", command=lambda: self.filter_tasks('year')).grid(row=8, column=3, padx=10, pady=5)

        # Légende
        self.legend_frame = tk.Frame(self.root)
        self.legend_frame.grid(row=9, column=3, columnspan=2, pady=10, sticky="se")
        self.create_legend()

    def create_legend(self):
        tk.Label(self.legend_frame, text="Légende des couleurs :", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w")
        for task_type, color in self.task_types.items():
            tk.Label(self.legend_frame, text=task_type, bg=color, width=20).grid(sticky="w")

    def add_task(self):
        task = self.task_entry.get()
        task_type = self.task_type.get()
        deadline_str = self.deadline_entry.get()

        if not deadline_str:
            messagebox.showwarning("Avertissement", "Veuillez entrer une date limite.")
            return

        try:
            # Convertir la date limite en format datetime pour le tri
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Avertissement", "Veuillez entrer une date valide au format YYYY-MM-DD.")
            return

        if task:
            # Ajouter la tâche avec son type, date limite et sans feedback initial
            self.tasks.append({"task": task, "type": task_type, "completed": False, "feedback": None, "deadline": deadline})
            self.update_task_lists()
            self.task_entry.delete(0, tk.END)
            self.deadline_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Avertissement", "Veuillez entrer une tâche.")

    def update_task_lists(self):
        # Vider les Listboxes et les mettre à jour
        self.todo_listbox.delete(0, tk.END)
        self.completed_listbox.delete(0, tk.END)

        for task_info in self.tasks:
            task_display = f"{task_info['task']} - [{task_info['type']}]"
            color = self.task_types.get(task_info["type"], "lightgrey")
            if task_info["deadline"]:
                task_display += f" - Date limite: {task_info['deadline'].strftime('%Y-%m-%d')}"
            if task_info["completed"]:
                if task_info["feedback"]:
                    task_display += f" - Feedback: {task_info['feedback']}"
                self.completed_listbox.insert(tk.END, task_display)
            else:
                self.todo_listbox.insert(tk.END, task_display)
                self.todo_listbox.itemconfig(tk.END, {'bg': color})

    def filter_tasks(self, timeframe):
        today_str = self.today_entry.get()
        try:
            today = datetime.strptime(today_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Avertissement", "Veuillez entrer une date valide pour aujourd'hui au format YYYY-MM-DD.")
            return

        filtered_tasks = []

        if timeframe == 'today':
            filtered_tasks = [task for task in self.tasks if task["deadline"] and task["deadline"].date() == today.date()]
        elif timeframe == 'week':
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6)
            filtered_tasks = [task for task in self.tasks if task["deadline"] and start_of_week <= task["deadline"] <= end_of_week]
        elif timeframe == 'month':
            filtered_tasks = [task for task in self.tasks if task["deadline"] and task["deadline"].month == today.month and task["deadline"].year == today.year]
        elif timeframe == 'year':
            filtered_tasks = [task for task in self.tasks if task["deadline"] and task["deadline"].year == today.year]

        self.todo_listbox.delete(0, tk.END)
        self.completed_listbox.delete(0, tk.END)

        for task_info in filtered_tasks:
            task_display = f"{task_info['task']} - [{task_info['type']}]"
            color = self.task_types.get(task_info["type"], "lightgrey")
            if task_info["deadline"]:
                task_display += f" - Date limite: {task_info['deadline'].strftime('%Y-%m-%d')}"
            self.todo_listbox.insert(tk.END, task_display)
            self.todo_listbox.itemconfig(tk.END, {'bg': color})

    def complete_task(self):
        selected_task_index = self.todo_listbox.curselection()
        if selected_task_index:
            task_info = self.tasks[selected_task_index[0]]
            feedback = simpledialog.askstring("Feedback", "Entrez votre feedback (laisser vide si aucun) :")
            task_info["completed"] = True
            task_info["feedback"] = feedback
            self.update_task_lists()
        else:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner une tâche à marquer comme terminée.")

    def delete_task(self):
        selected_task_index = self.todo_listbox.curselection()
        if selected_task_index:
            del self.tasks[selected_task_index[0]]
            self.update_task_lists()
        else:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner une tâche à supprimer.")

    def resize_widgets(self, event):
        # Ajuster la taille des widgets en fonction de la taille de la fenêtre
        self.scale_factor = min(event.width / 1000, event.height / 600)
        new_width = int(50 * self.scale_factor)
        self.todo_listbox.config(width=new_width)
        self.completed_listbox.config(width=new_width)

if __name__ == "__main__":
    root = tk.Tk()
    app = FlightTestTaskManager(root)
    root.mainloop()
