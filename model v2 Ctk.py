import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta
from tkinter import simpledialog

class FlightTestTaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestionnaire de Tâches - Tests en Vol")
        self.root.geometry("1200x700")
        
        ctk.set_appearance_mode("light")
        
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

        self.create_widgets()
    
    def toggle_theme(self):
        if self.current_theme == self.light_theme:
            self.current_theme = self.dark_theme
            ctk.set_appearance_mode("dark")
        else:
            self.current_theme = self.light_theme
            ctk.set_appearance_mode("light")
        
        self.update_theme()

    def update_theme(self):
        self.root.configure(bg=self.current_theme["bg"])

        for button in self.root.winfo_children():
            if isinstance(button, ctk.CTkButton):
                button.configure(fg_color=self.current_theme["button_bg"], text_color=self.current_theme["button_fg"])

        for widget in self.task_frame.winfo_children():
            widget.configure(bg=self.current_theme["bg"], fg=self.current_theme["fg"])

        for widget in self.todo_list_frame.winfo_children():
            widget.configure(bg=self.current_theme["task_bg"], fg=self.current_theme["task_fg"])

        for widget in self.completed_list_frame.winfo_children():
            widget.configure(bg=self.current_theme["task_bg"], fg=self.current_theme["task_fg"])

    def create_widgets(self):
        ctk.CTkLabel(self.root, text="Gestionnaire de Tâches - Tests en Vol", font=("Arial", 24, "bold")).pack(pady=10)

        self.task_frame = ctk.CTkFrame(self.root, corner_radius=15)
        self.task_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(self.task_frame, text="Nouvelle tâche :", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.task_entry = ctk.CTkEntry(self.task_frame, width=300, placeholder_text="Entrez une description...")
        self.task_entry.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(self.task_frame, text="Type de tâche :", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.task_type = ctk.StringVar(self.root)
        self.task_type.set("Préparation du vol")
        self.task_type_menu = ctk.CTkOptionMenu(self.task_frame, variable=self.task_type, values=list(self.task_types.keys()))
        self.task_type_menu.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        ctk.CTkLabel(self.task_frame, text="Date limite (YYYY-MM-DD) :", font=("Arial", 14)).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.deadline_entry = ctk.CTkEntry(self.task_frame, width=200, placeholder_text="YYYY-MM-DD")
        self.deadline_entry.grid(row=2, column=1, padx=10, pady=10)

        ctk.CTkLabel(self.task_frame, text="Date d'aujourd'hui :", font=("Arial", 14)).grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.today_entry = ctk.CTkEntry(self.task_frame, width=200)
        self.today_entry.insert(0, self.today.strftime("%Y-%m-%d"))
        self.today_entry.grid(row=3, column=1, padx=10, pady=10)

        ctk.CTkButton(self.task_frame, text="Ajouter Tâche", command=self.add_task).grid(row=4, column=1, pady=10)

        self.list_frame = ctk.CTkFrame(self.root, corner_radius=15)
        self.list_frame.pack(pady=10, padx=20, fill="both", expand=True)

        ctk.CTkLabel(self.list_frame, text="À faire :", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=10, pady=10)
        self.todo_list_frame = ctk.CTkFrame(self.list_frame)
        self.todo_list_frame.grid(row=1, column=0, padx=10, pady=10)

        ctk.CTkLabel(self.list_frame, text="Terminées :", font=("Arial", 14, "bold")).grid(row=0, column=1, padx=10, pady=10)
        self.completed_list_frame = ctk.CTkFrame(self.list_frame)
        self.completed_list_frame.grid(row=1, column=1, padx=10, pady=10)

        self.button_frame = ctk.CTkFrame(self.root, corner_radius=15)
        self.button_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkButton(self.button_frame, text="Marquer comme Terminée", command=self.mark_task_completed).pack(side="left", padx=10, pady=10)
        ctk.CTkButton(self.button_frame, text="Supprimer Tâche", command=self.delete_task).pack(side="left", padx=10, pady=10)
        ctk.CTkButton(self.button_frame, text="Tâches d'Aujourd'hui", command=lambda: self.filter_tasks("today")).pack(side="left", padx=10, pady=10)
        ctk.CTkButton(self.button_frame, text="Afficher toutes les tâches", command=self.show_all_tasks).pack(side="left", padx=10, pady=10)
        ctk.CTkButton(self.button_frame, text="Changer le Thème", command=self.toggle_theme).pack(side="left", padx=10, pady=10)
        ctk.CTkButton(self.button_frame, text="Filtrer par Couleur", command=self.filter_tasks_by_color).pack(side="left", padx=10, pady=10)

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
            self.update_task_lists()
        else:
            messagebox.showwarning("Avertissement", "Indice invalide.")

    def delete_task_from_list(self, idx):
        del self.tasks[idx]
        self.update_task_lists()

    def mark_task_completed(self, idx):
        feedback = simpledialog.askstring("Feedback", f"Merci d'avoir terminé la tâche '{self.tasks[idx]['task']}'. Comment évalueriez-vous cette tâche ?")
        
        self.tasks[idx]["completed"] = True
        self.tasks[idx]["feedback"] = feedback if feedback else "Aucun retour fourni."
        
        self.update_task_lists()


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
            end_of_week = today + timedelta(days=6)
            filtered_tasks = [task for task in self.tasks if task["deadline"] and today <= task["deadline"] <= end_of_week]
        elif timeframe == 'month':
            filtered_tasks = [task for task in self.tasks if task["deadline"] and task["deadline"].month == today.month and task["deadline"].year == today.year]

        self.todo_listbox.delete("1.0", ctk.END)
        for task_info in filtered_tasks:
            task_display = f"{task_info['task']} - [{task_info['type']}] - Date limite: {task_info['deadline'].strftime('%Y-%m-%d')}"
            self.todo_listbox.insert(ctk.END, task_display + "\n")

    def show_all_tasks(self):
        self.update_task_lists()


if __name__ == "__main__":
    root = ctk.CTk()
    app = FlightTestTaskManager(root)
    root.mainloop()
