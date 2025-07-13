import tkinter as tk #bibliothèque Python standard pour la création d'interfaces graphiques
from tkinter import ttk
from PIL import Image, ImageTk  # Import from Pillow library
import subprocess
import os

class App:
    def __init__(self, root): #root fenêtre racine
        self.root = root
        self.root.title("Script Switcher")
        self.root.geometry("4096x3000")

        # Load and add a logo to the main window
        logo_path = "logo.png"
        if os.path.exists(logo_path):
            logo_image = self.load_image(logo_path)
            logo_label = ttk.Label(self.root, image=logo_image)
            logo_label.image = logo_image  # Keep a reference to avoid garbage collection
            logo_label.pack()

        # Add a large title below the logo with a specific color
        title_label = ttk.Label(self.root, text="Vision system", font=("Arial", 80, "bold"), foreground="blue")
        title_label.pack(side=tk.TOP, padx=10, pady=10)  # Adjust padx and pady as needed
 

        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True) #redimensionner le cadre pour qu'il remplisse tout l'espace disponible dans la fenêtre principale à la fois horizontalement et verticalement

        self.button_frame = ttk.Frame(self.frame) ##contenir les boutons de l'interface utilisateur
        self.button_frame.pack(side=tk.LEFT, fill=tk.Y) # placer le cadre des boutons à gauche du cadre principal et redimensionner le cadre des boutons uniquement verticalement pour qu'il remplisse toute la hauteur disponible dans le cadre principal

        # Define the paths for each script
        script_paths = {"Capture": r"C:\Users\iram trabelsi\Pictures\FF\automatic.py","Mode Automatique": r"C:\Users\iram trabelsi\Pictures\FF\camera.py","Mode Manuel": r"C:\Users\iram trabelsi\Pictures\FF\measurment.py"}
        #liste utilisée pour stocker les boutons de script créés dynamiquement.
        self.script_buttons = []

        for text, path in script_paths.items():
            button = ttk.Button(self.button_frame, text=text, command=lambda p=path: self.run_script(p))
            button.pack(fill=tk.X)
            self.script_buttons.append(button)

    def load_image(self, path):
        image = Image.open(path)
        image = ImageTk.PhotoImage(image) #convertir l'image en un format compatible avec Tkinter
        return image

    def run_script(self, path):
         #creation une nouvelle fenêtre
        new_window = tk.Toplevel(self.root) #toplevel creer une fenêtre indépendante 
        new_window.title("Script Window")
        new_window.geometry("800x600")  # Adjust the size as needed

        # Create a frame in the new window
        frame = ttk.Frame(new_window)
        frame.pack(fill=tk.BOTH, expand=True)

        # Add buttons for switching between scripts in the new window
        switch_buttons = [] #Une liste vide est créée pour stocker les boutons de commutation qui seront créés
        for btn in self.script_buttons:
            switch_button = ttk.Button(frame, text=btn["text"], command=lambda p=btn.cget("command"): self.run_script(p))
            switch_button.pack(side=tk.LEFT)
            switch_buttons.append(switch_button)

        # Add a label or other widgets to the frame
        label = ttk.Label(frame, text=f"Running script: {os.path.basename(path)}")
        label.pack()

        # Run the selected script
        subprocess.Popen(["python", path])
        # Close the main window
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
