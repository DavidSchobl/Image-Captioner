import tkinter as tk
from tkinter import filedialog, Text
import os
from PIL import Image, ImageTk
import glob

class ImageViewerEditor:
    def __init__(self, root):
        # Inicializace hlavního okna aplikace
        self.root = root
        self.current_image_path = ''  # Aktuální cesta k obrázku
        self.image_paths = []  # Seznam cest k obrázkům ve vybrané složce
        self.current_index = 0  # Index aktuálně zobrazeného obrázku

        self.setup_ui()  # Nastavení uživatelského rozhraní

    def setup_ui(self):
        # Nastavení titulku a velikosti hlavního okna
        self.root.title("Image Captioner for AI training")
        self.root.geometry("800x400")

        # Tlačítko pro otevření dialogu pro výběr složky
        self.open_folder_btn = tk.Button(self.root, text="Open Folder", command=self.open_folder)
        self.open_folder_btn.pack()

        # Label pro zobrazení vybrané cesty
        self.path_label = tk.Label(self.root, text="")
        self.path_label.pack()

        # Hlavní rám pro obrázek a textový editor
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=10)

        # Rám pro obrázek s pevnou velikostí a šedým pozadím
        self.image_frame = tk.Frame(self.main_frame, width=250, height=250, bg='grey')
        self.image_frame.pack(side=tk.LEFT, padx=(0,20))
        self.image_frame.pack_propagate(False)  # Zabrání změně velikosti rámce podle obsahu

        # Label pro zobrazení obrázku
        self.image_label = tk.Label(self.image_frame, bg='grey')
        self.image_label.pack(expand=True)

        # Textový editor pro zobrazení a úpravu textu
        self.text_editor = tk.Text(self.main_frame, height=15, width=50)
        self.text_editor.pack(side=tk.RIGHT)

        # Rám pro navigační tlačítka
        self.navigation_frame = tk.Frame(self.root)
        self.navigation_frame.pack(pady=(10,0))

        # Tlačítka pro navigaci mezi obrázky
        self.prev_button = tk.Button(self.navigation_frame, text="Previous", command=self.show_previous, height=2, width=10)
        self.prev_button.pack(side=tk.LEFT, padx=5)

        self.next_button = tk.Button(self.navigation_frame, text="Next", command=self.show_next, height=2, width=10)
        self.next_button.pack(side=tk.LEFT, padx=5)

    def open_folder(self):
        # Funkce pro otevření dialogu a výběr složky
        folder_selected = filedialog.askdirectory()
        self.path_label.config(text=folder_selected)
        if folder_selected:
            self.image_paths = sorted(glob.glob(os.path.join(folder_selected, "*.png")))
            self.current_index = 0
            if self.image_paths:
                self.show_image_and_text()

    def show_image_and_text(self):
        # Zobrazení obrázku a příslušného textového souboru
        if self.image_paths:
            self.current_image_path = self.image_paths[self.current_index]
            img = Image.open(self.current_image_path)
            img.thumbnail((self.image_frame.winfo_width(), self.image_frame.winfo_height()))

            photo = ImageTk.PhotoImage(img)
            self.image_label.config(image=photo)
            self.image_label.image = photo
            self.image_label.pack(expand=True)

            text_file_path = self.current_image_path.replace('.png', '.txt')
            if os.path.exists(text_file_path):
                with open(text_file_path, 'r') as file:
                    data = file.read()
                    self.text_editor.delete(1.0, tk.END)
                    self.text_editor.insert(tk.END, data)
            else:
                self.text_editor.delete(1.0, tk.END)

    def show_next(self):
        # Přechod k dalšímu obrázku
        if self.current_index < len(self.image_paths) - 1:
            self.save_text_file()
            self.current_index += 1
            self.show_image_and_text()

    def show_previous(self):
        # Přechod k předchozímu obrázku
        if self.current_index > 0:
            self.save_text_file()
            self.current_index -= 1
            self.show_image_and_text()

    def save_text_file(self):
        # Uložení změn v textovém souboru
        text_file_path = self.current_image_path.replace('.png', '.txt')
        with open(text_file_path, 'w') as file:
            file.write(self.text_editor.get(1.0, tk.END))

if __name__ == "__main__":
    # Spuštění aplikace
    root = tk.Tk()
    app = ImageViewerEditor(root)
    root.mainloop()
