import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from tkinter import simpledialog
import json
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



class FlightTestTaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestionnaire de Tâches - Tests en Vol")
        self.root.geometry("1200x700")

        ctk.set_appearance_mode("light")
        
        # Définitions des langues
        self.languages = {
            "fr": {
                "title": "Gestionnaire de Tâches - Tests en Vol",
                "new_task": "Nouvelle tâche :",
                "task_type": "Type de tâche :",
                "deadline": "Date limite (YYYY-MM-DD) :",
                "today": "Date d'aujourd'hui :",
                "add_task": "Ajouter Tâche",
                "todo": "À faire :",
                "completed": "Terminées :",
                "tasks_today": "Tâches d'Aujourd'hui",
                "show_all": "Afficher toutes les tâches",
                "change_theme": "Changer le Thème",
                "filter_color": "Filtrer par Couleur",
                "chart_completion": "Graphique: Tâches terminées",
                "chart_types": "Graphique: Répartition des couleurs"
            },
            "en": {
                "title": "Task Manager - Flight Tests",
                "new_task": "New Task:",
                "task_type": "Task Type:",
                "deadline": "Deadline (YYYY-MM-DD):",
                "today": "Today's Date:",
                "add_task": "Add Task",
                "todo": "To Do:",
                "completed": "Completed:",
                "tasks_today": "Today's Tasks",
                "show_all": "Show All Tasks",
                "change_theme": "Change Theme",
                "filter_color": "Filter by Color",
                "chart_completion": "Chart: Completed Tasks",
                "chart_types": "Chart: Task Types Distribution"
            }
        }
        self.current_language = "fr"  # Langue par défaut

        self.light_theme = {
            "bg": "#f0f0f0",
            "fg": "#000000",
            "task_bg": "#AEDFF7",
            "task_fg": "#000000",
            "button_bg": "#D4F7AE",
            "button_fg": "#000000"
        }
        
        self.dark_theme = {
            "bg": "#2b2b2b",
            "fg": "#ffffff",
            "task_bg": "#1c1c1c",
            "task_fg": "#ffffff",
            "button_bg": "#4F4F4F",
            "button_fg": "#ffffff"
        }

        self.current_theme = self.light_theme
        self.task_types = {
            "Préparation du vol": "#AEDFF7",
            "Installation de l'équipement": "#D4F7AE",
            "Collecte de données": "#F7B4A6",
            "Analyse post-vol": "#D3D3D3"
        }
        self.tasks = []
        self.today = datetime.now()
        
        self.load_tasks_from_json()  # Chargement des tâches
        self.create_widgets()
        self.update_task_lists()

    def toggle_language(self):
        """Basculer entre les langues et mettre à jour l'interface"""
        self.current_language = "en" if self.current_language == "fr" else "fr"
        self.update_language()

    def update_language(self):
        """Mettre à jour tous les textes de l'interface"""
        lang = self.languages[self.current_language]
        self.root.title(lang["title"])
        self.task_label.configure(text=lang["new_task"])
        self.type_label.configure(text=lang["task_type"])
        self.deadline_label.configure(text=lang["deadline"])
        self.today_label.configure(text=lang["today"])
        self.add_task_button.configure(text=lang["add_task"])
        self.todo_label.configure(text=lang["todo"])
        self.completed_label.configure(text=lang["completed"])
        self.tasks_today_button.configure(text=lang["tasks_today"])
        self.show_all_button.configure(text=lang["show_all"])
        self.change_theme_button.configure(text=lang["change_theme"])
        self.filter_color_button.configure(text=lang["filter_color"])
        self.chart_completion_button.configure(text=lang["chart_completion"])
        self.chart_types_button.configure(text=lang["chart_types"])

    def create_widgets(self):
        # Ajout des widgets principaux
        lang = self.languages[self.current_language]

        self.task_label = ctk.CTkLabel(self.root, text=lang["title"], font=("Arial", 24, "bold"))
        self.task_label.pack(pady=10)

        self.task_frame = ctk.CTkFrame(self.root, corner_radius=15)
        self.task_frame.pack(pady=10, padx=20, fill="x")

        self.task_label = ctk.CTkLabel(self.task_frame, text=lang["new_task"], font=("Arial", 14))
        self.task_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.task_entry = ctk.CTkEntry(self.task_frame, width=300, placeholder_text="Entrez une description...")
        self.task_entry.grid(row=0, column=1, padx=10, pady=10)

        self.type_label = ctk.CTkLabel(self.task_frame, text=lang["task_type"], font=("Arial", 14))
        self.type_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.task_type = ctk.StringVar(self.root)
        self.task_type.set("Préparation du vol")
        self.task_type_menu = ctk.CTkOptionMenu(self.task_frame, variable=self.task_type, values=list(self.task_types.keys()))
        self.task_type_menu.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        self.deadline_label = ctk.CTkLabel(self.task_frame, text=lang["deadline"], font=("Arial", 14))
        self.deadline_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.deadline_entry = ctk.CTkEntry(self.task_frame, width=200, placeholder_text="YYYY-MM-DD")
        self.deadline_entry.grid(row=2, column=1, padx=10, pady=10)

        self.today_label = ctk.CTkLabel(self.task_frame, text=lang["today"], font=("Arial", 14))
        self.today_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.today_entry = ctk.CTkEntry(self.task_frame, width=200)
        self.today_entry.insert(0, self.today.strftime("%Y-%m-%d"))
        self.today_entry.grid(row=3, column=1, padx=10, pady=10)

        self.add_task_button = ctk.CTkButton(self.task_frame, text=lang["add_task"], command=self.add_task)
        self.add_task_button.grid(row=4, column=1, pady=10)

        # Bouton pour changer de langue
        self.lang_button = ctk.CTkButton(self.task_frame, text="Changer Langue", command=self.toggle_language)
        self.lang_button.grid(row=4, column=2, pady=10)

    def save_tasks_to_json(self):
        tasks_to_save = [
            {
                "task": task["task"],
                "type": task["type"],
                "completed": task["completed"],
                "deadline": task["deadline"].strftime("%Y-%m-%d"),
                "feedback": task.get("feedback", "")
            }
            for task in self.tasks
        ]
        with open('tasks.json', 'w') as json_file:
            json.dump(tasks_to_save, json_file, indent=4)


    def load_tasks_from_json(self):
        if os.path.exists('tasks.json'):
            try:
                with open('tasks.json', 'r') as json_file:
                    tasks_data = json.load(json_file)
                    
                # Convert string dates back to datetime.date objects
                self.tasks = [
                    {
                        "task": task["task"],
                        "type": task["type"],
                        "completed": task["completed"],
                        "deadline": datetime.strptime(task["deadline"], "%Y-%m-%d").date(),
                        "feedback": task.get("feedback", "Aucun retour fourni.")
                    }
                    for task in tasks_data
                ]
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                messagebox.showerror("Erreur de Chargement", f"Erreur dans le fichier JSON : {e}")
                self.tasks = []  # Charger une liste vide en cas d'erreur
        else:
            self.tasks = []  # Pas de fichier JSON, initialiser une liste vide

    
    def toggle_theme(self):
        if self.current_theme == self.light_theme:
            self.current_theme = self.dark_theme
            ctk.set_appearance_mode("dark")
        else:
            self.current_theme = self.light_theme
            ctk.set_appearance_mode("light")
        
        self.update_theme()


    def add_task(self):
        task = self.task_entry.get()
        task_type = self.task_type.get()
        deadline_str = self.deadline_entry.get()

        if not deadline_str:
            messagebox.showwarning("Avertissement", "Veuillez entrer une date limite.")
            return

        try:
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Avertissement", "Veuillez entrer une date valide au format YYYY-MM-DD.")
            return

        if task:
            self.tasks.append({"task": task, "type": task_type, "completed": False, "deadline": deadline})
            self.save_tasks_to_json()  # Save tasks to JSON after adding
            self.update_task_lists()
            self.task_entry.delete(0, ctk.END)
            self.deadline_entry.delete(0, ctk.END)
        else:
            messagebox.showwarning("Avertissement", "Veuillez entrer une tâche.")

    def update_task_lists(self):
        for widget in self.todo_list_frame.winfo_children():
            widget.destroy()
        for widget in self.completed_list_frame.winfo_children():
            widget.destroy()

        for idx, task_info in enumerate(self.tasks):
            task_display = f"{task_info['task']} - [{task_info['type']}] - Date limite: {task_info['deadline'].strftime('%Y-%m-%d')}"
            task_color = self.task_types[task_info['type']]

            if not task_info["completed"]:
                task_frame = ctk.CTkFrame(self.todo_list_frame, fg_color=task_color)
                task_frame.pack(fill="x", pady=5)
                ctk.CTkLabel(task_frame, text=task_display).pack(side="left", padx=10)
                complete_button = ctk.CTkButton(task_frame, text="Terminer", command=lambda idx=idx: self.mark_task_completed(idx))
                complete_button.pack(side="right", padx=10)
                delete_button = ctk.CTkButton(task_frame, text="Supprimer", command=lambda idx=idx: self.delete_task_from_list(idx))
                delete_button.pack(side="right", padx=10)

        for task_info in self.tasks:
            if task_info["completed"]:
                task_display = f"{task_info['task']} - [{task_info['type']}] - Date limite: {task_info['deadline'].strftime('%Y-%m-%d')} - Retour: {task_info.get('feedback', 'Aucun retour fourni.')}"
                task_color = self.task_types[task_info['type']]
                task_frame = ctk.CTkFrame(self.completed_list_frame, fg_color=task_color)
                task_frame.pack(fill="x", pady=5)
                ctk.CTkLabel(task_frame, text=task_display).pack(side="left", padx=10)

    def delete_task(self):
        task_index = simpledialog.askinteger("Tâche", "Entrez l'indice de la tâche à supprimer :")
        if task_index is not None and 0 <= task_index < len(self.tasks):
            del self.tasks[task_index]
            self.save_tasks_to_json()  # Save tasks to JSON after deletion
            self.update_task_lists()
        else:
            messagebox.showwarning("Avertissement", "Indice invalide.")

    def delete_task_from_list(self, idx):
        del self.tasks[idx]
        self.save_tasks_to_json()  # Save tasks to JSON after deletion
        self.update_task_lists()

    def mark_task_completed(self, idx):
        feedback = simpledialog.askstring("Feedback", f"Merci d'avoir terminé la tâche '{self.tasks[idx]['task']}'. Comment évalueriez-vous cette tâche ?")
        
        self.tasks[idx]["completed"] = True
        self.tasks[idx]["feedback"] = feedback if feedback else "Aucun retour fourni."
        
        self.save_tasks_to_json()  # Save tasks to JSON after marking as completed
        self.update_task_lists()

    def filter_tasks(self, timeframe):
        today_str = self.today_entry.get()
        try:
            today = datetime.strptime(today_str, "%Y-%m-%d").date()  # Convertir en date
        except ValueError:
            messagebox.showwarning("Avertissement", "Veuillez entrer une date valide pour aujourd'hui au format YYYY-MM-DD.")
            return

        filtered_tasks = []

        if timeframe == 'today':
            # Comparer directement avec la date d'aujourd'hui
            filtered_tasks = [task for task in self.tasks if task["deadline"] == today]  # Assurez-vous que task["deadline"] est de type date

            if not filtered_tasks:
                messagebox.showinfo("Information", "Aucune tâche prévue pour aujourd'hui.")
                return

        # Effacer les listes de tâches affichées
        for widget in self.todo_list_frame.winfo_children():
            widget.destroy()
        for widget in self.completed_list_frame.winfo_children():
            widget.destroy()

        # Afficher les tâches filtrées
        for idx, task_info in enumerate(filtered_tasks):
            task_display = f"{task_info['task']} - [{task_info['type']}] - Date limite: {task_info['deadline'].strftime('%Y-%m-%d')}"
            task_color = self.task_types[task_info['type']]

            if not task_info["completed"]:
                task_frame = ctk.CTkFrame(self.todo_list_frame, fg_color=task_color)
                task_frame.pack(fill="x", pady=5)
                ctk.CTkLabel(task_frame, text=task_display).pack(side="left", padx=10)
                complete_button = ctk.CTkButton(task_frame, text="Terminer", command=lambda idx=idx: self.mark_task_completed(idx))
                complete_button.pack(side="right", padx=10)
                delete_button = ctk.CTkButton(task_frame, text="Supprimer", command=lambda idx=idx: self.delete_task_from_list(idx))
                delete_button.pack(side="right", padx=10)

            else:
                task_frame = ctk.CTkFrame(self.completed_list_frame, fg_color=task_color)
                task_frame.pack(fill="x", pady=5)
                ctk.CTkLabel(task_frame, text=task_display).pack(side="left", padx=10)

    def filter_tasks_by_color(self):
        color = simpledialog.askstring("Couleur", "Entrez la couleur de la tâche à filtrer (ex: Préparation du vol, Installation de l'équipement, Collecte de données, Analyse post-vol) :")
        
        if color not in self.task_types:
            messagebox.showwarning("Avertissement", "Couleur invalide. Veuillez entrer une couleur valide.")
            return

        filtered_tasks = [task for task in self.tasks if task["type"] == color]

        for widget in self.todo_list_frame.winfo_children():
            widget.destroy()
        for widget in self.completed_list_frame.winfo_children():
            widget.destroy()

        for idx, task_info in enumerate(filtered_tasks):
            task_display = f"{task_info['task']} - [{task_info['type']}] - Date limite: {task_info['deadline'].strftime('%Y-%m-%d')}"
            task_color = self.task_types[task_info['type']]

            if not task_info["completed"]:
                task_frame = ctk.CTkFrame(self.todo_list_frame, fg_color=task_color)
                task_frame.pack(fill="x", pady=5)
                ctk.CTkLabel(task_frame, text=task_display).pack(side="left", padx=10)
                complete_button = ctk.CTkButton(task_frame, text="Terminer", command=lambda idx=idx: self.mark_task_completed(idx))
                complete_button.pack(side="right", padx=10)
                delete_button = ctk.CTkButton(task_frame, text="Supprimer", command=lambda idx=idx: self.delete_task_from_list(idx))
                delete_button.pack(side="right", padx=10)

            else:
                task_frame = ctk.CTkFrame(self.completed_list_frame, fg_color=task_color)
                task_frame.pack(fill="x", pady=5)
                ctk.CTkLabel(task_frame, text=task_display).pack(side="left", padx=10)

    def show_all_tasks(self):
        self.update_task_lists()

    def show_task_completion_pie_chart(self):
        # Comptage des tâches terminées et non terminées
        completed_tasks = sum(1 for task in self.tasks if task["completed"])
        pending_tasks = len(self.tasks) - completed_tasks
        
        # Création du graphique
        labels = ["Terminées", "À faire"]
        sizes = [completed_tasks, pending_tasks]
        colors = ["#4CAF50", "#FF5722"]
        
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.pie(sizes, labels=labels, autopct="%1.1f%%", colors=colors, startangle=90)
        ax.set_title("Proportion des tâches terminées")

        # Afficher le graphique dans une nouvelle fenêtre
        self.display_chart(fig)

    def show_task_type_pie_chart(self):
        # Comptage des tâches à faire par type
        task_type_counts = {task_type: 0 for task_type in self.task_types}
        for task in self.tasks:
            if not task["completed"]:
                task_type_counts[task["type"]] += 1
        
        # Création du graphique
        labels = list(task_type_counts.keys())
        sizes = list(task_type_counts.values())
        colors = [self.task_types[task_type] for task_type in task_type_counts]

        fig, ax = plt.subplots(figsize=(4, 4))
        ax.pie(sizes, labels=labels, autopct="%1.1f%%", colors=colors, startangle=90)
        ax.set_title("Répartition des types de tâches à faire")

        # Afficher le graphique dans une nouvelle fenêtre
        self.display_chart(fig)

    def display_chart(self, fig):
        # Créer une nouvelle fenêtre pour afficher le graphique
        chart_window = ctk.CTkToplevel(self.root)
        chart_window.title("Graphique")

        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill="both", expand=True)
        canvas.draw()




if __name__ == "__main__":
    root = ctk.CTk()
    app = FlightTestTaskManager(root)
    root.mainloop()