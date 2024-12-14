import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from Image_processing_Project import ImageProcessor  # Import from first file


class ImageProcessingApp:
    def __init__(self, master):
        self.master = master
        master.title("Image Processing App")
        master.geometry("800x600")

        # Create ImageProcessor instance
        self.processor = ImageProcessor()

        # Image variables
        self.current_image = None
        self.original_image = None

        # Create UI
        self.create_widgets()

    def create_widgets(self):
        # Buttons Frame
        btn_frame = tk.Frame(self.master)
        btn_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Button definitions
        buttons = [
            ("Load Image", self.load_image),
            ("Grayscale", self.apply_grayscale),
            ("Blur", self.apply_blur),
            ("Brighten", self.adjust_brightness),
            ("Edge Detect", self.detect_edges),
            ("Reset", self.reset_image)
        ]

        # Create buttons
        for text, command in buttons:
            btn = tk.Button(btn_frame, text=text, command=command)
            btn.pack(side=tk.LEFT, padx=5)

        # Image Display Label
        self.image_label = tk.Label(self.master)
        self.image_label.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    def load_image(self):
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )

        if file_path:
            try:
                self.original_image = self.processor.load_image(file_path)
                self.current_image = self.original_image.copy()
                self.display_image()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def display_image(self):
        if self.current_image:
            # Resize image
            img_copy = self.current_image.copy()
            img_copy.thumbnail((700, 500), Image.LANCZOS)

            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(img_copy)
            self.image_label.config(image=photo)
            self.image_label.image = photo  # Keep a reference

    def apply_grayscale(self):
        if self.current_image:
            self.current_image = self.processor.apply_grayscale(self.current_image)
            self.display_image()

    def apply_blur(self):
        if self.current_image:
            self.current_image = self.processor.apply_blur(self.current_image)
            self.display_image()

    def adjust_brightness(self):
        if self.current_image:
            self.current_image = self.processor.adjust_brightness(self.current_image)
            self.display_image()

    def detect_edges(self):
        if self.current_image:
            self.current_image = self.processor.detect_edges(self.current_image)
            self.display_image()

    def reset_image(self):
        if self.original_image:
            self.current_image = self.original_image.copy()
            self.display_image()