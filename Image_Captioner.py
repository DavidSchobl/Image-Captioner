
import tkinter as tk
from tkinter import filedialog, Text
import os
from PIL import Image, ImageTk
import glob
from transformers import BlipProcessor, BlipForConditionalGeneration
import warnings

warnings.filterwarnings("ignore", message="TypedStorage is deprecated")

class ImageViewerEditor:
    def __init__(self, root):
        self.root = root
        self.current_image_path = ''
        self.image_paths = []
        self.current_index = 0

        # Načtení BLIP modelu a procesoru
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

        self.setup_ui()

    def setup_ui(self):
        self.root.title("Image Captioner for AI training")
        self.root.geometry("800x400")

        self.open_folder_btn = tk.Button(self.root, text="Open Folder", command=self.open_folder)
        self.open_folder_btn.pack()

        self.path_label = tk.Label(self.root, text="")
        self.path_label.pack()

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=10)

        self.image_frame = tk.Frame(self.main_frame, width=250, height=250, bg='grey')
        self.image_frame.pack(side=tk.LEFT, padx=(0,20))
        self.image_frame.pack_propagate(False)

        self.image_label = tk.Label(self.image_frame, bg='grey')
        self.image_label.pack(expand=True)

        self.text_editor = tk.Text(self.main_frame, height=15, width=50)
        self.text_editor.pack(side=tk.RIGHT)

        self.navigation_frame = tk.Frame(self.root)
        self.navigation_frame.pack(pady=(10,0))

        self.prev_button = tk.Button(self.navigation_frame, text="Previous", command=self.show_previous, height=2, width=10)
        self.prev_button.pack(side=tk.LEFT, padx=5)

        self.next_button = tk.Button(self.navigation_frame, text="Next", command=self.show_next, height=2, width=10)
        self.next_button.pack(side=tk.LEFT, padx=5)

        # Tlačítko pro generování popisku BLIP
        self.blip_it_btn = tk.Button(self.navigation_frame, text="BLIP IT!", command=self.generate_caption_with_blip, height=2, width=10)
        self.blip_it_btn.pack(side=tk.LEFT, padx=10)

    def open_folder(self):
        folder_selected = filedialog.askdirectory()
        self.path_label.config(text=folder_selected)
        if folder_selected:
            self.image_paths = sorted(glob.glob(os.path.join(folder_selected, "*.png")))
            self.current_index = 0
            if self.image_paths:
                self.show_image_and_text()

    def show_image_and_text(self):
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
        if self.current_index < len(self.image_paths) - 1:
            self.save_text_file()
            self.current_index += 1
            self.show_image_and_text()

    def show_previous(self):
        if self.current_index > 0:
            self.save_text_file()
            self.current_index -= 1
            self.show_image_and_text()

    def save_text_file(self):
        text_file_path = self.current_image_path.replace('.png', '.txt')
        with open(text_file_path, 'w') as file:
            file.write(self.text_editor.get(1.0, tk.END))

    def generate_caption_with_blip(self):
        # Generování popisku pomocí BLIP
        if self.current_image_path:
            img = Image.open(self.current_image_path).convert("RGB")
            inputs = self.processor(img, return_tensors="pt")
            outputs = self.model.generate(**inputs, max_new_tokens=200, do_sample=True, temperature=0.9, top_k=50, top_p=0.95)
            caption = self.processor.decode(outputs[0], skip_special_tokens=True)

            # Zobrazení vygenerovaného popisku v textovém editoru
            self.text_editor.delete(1.0, tk.END)
            self.text_editor.insert(tk.END, caption)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageViewerEditor(root)
    root.mainloop()
