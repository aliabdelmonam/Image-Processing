import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
from Image_processing_Project import ImageProcessor  # Import from first file


class ImageProcessingApp:
    def __init__(self, master):
        self.master = master
        master.title("Advanced Image Processing")
        master.geometry("1000x700")

        # Image processor
        self.processor = ImageProcessor()

        # Original image and processing history
        self.original_image = None
        self.img=None
        self.processed_images = []

        # Create main notebook (tabbed interface)
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create initial tab for main controls
        self.create_main_tab()

    def create_main_tab(self):
        # Main processing tab
        main_frame = ttk.Frame(self.notebook)
        self.notebook.add(main_frame, text="Main")

        # Buttons Frame
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Action Buttons
        buttons = [
            ("Load Image", self.load_image),
            ("Blur", self.create_blur_view),
            ("Grayscale", self.create_grayscale_view),
            ("Enhance", self.create_enhance_view),
            ("Reset",self.create_reset_button)
        ]

        for text, command in buttons:
            btn = tk.Button(btn_frame, text=text, command=command)
            btn.pack(side=tk.LEFT, padx=5)

        # Main Image Display
        self.main_image_label = tk.Label(main_frame)
        self.main_image_label.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    def load_image(self):
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )

        if file_path:
            try:
                # Load original image
                self.original_image = self.processor.load_image(file_path)
                self.img = self.original_image
                # Display in main tab
                self.display_image(self.img, self.main_image_label)

                # Reset processed images
                self.processed_images = []
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def display_image(self, image, label):
        if image:
            # Resize image
            img_copy = image.copy()
            img_copy.thumbnail((700, 500), Image.LANCZOS)

            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(img_copy)
            label.config(image=photo)
            label.image = photo  # Keep a reference


    def create_reset_button(self):
        if not self.img:
            messagebox.showwarning("Warning", "No image to reset!")
            return
        # Create a Reset button and add it to the UI

        self.img = self.original_image
        self.display_image(self.img, self.main_image_label)




    def create_blur_view(self):
        if not self.img:
            messagebox.showwarning("Warning", "Please load an image first!")
            return

        # Create blur processing tab
        blur_frame = ttk.Frame(self.notebook)
        self.notebook.add(blur_frame, text="Blur Processing")

        # Blur intensity slider
        slider_frame = tk.Frame(blur_frame)
        slider_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        tk.Label(slider_frame, text="Blur Intensity:").pack(side=tk.LEFT)
        blur_intensity = tk.Scale(
            slider_frame,
            from_=0,
            to=10,
            orient=tk.HORIZONTAL,
            length=300
        )
        blur_intensity.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # Image label for blur preview
        blur_image_label = tk.Label(blur_frame)
        blur_image_label.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Buttons frame
        btn_frame = tk.Frame(blur_frame)
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        # Apply Blur Button
        self.display_image(self.img, blur_image_label)
        def apply_blur():
            intensity = blur_intensity.get()
            blurred_image = self.processor.apply_blur(
                self.img,
                radius=intensity
            )
            self.img = blurred_image
            # Display blurred image
            self.display_image(self.img, blur_image_label)
            self.display_image(self.img, self.main_image_label)
            # Store processed image
            self.processed_images.append(blurred_image)

        # Return to Main Button
        def return_to_main():
            # Switch to main tab
            self.notebook.select(0)

            # Remove current tab
            self.notebook.forget(blur_frame)

        # Create buttons
        apply_btn = tk.Button(btn_frame, text="Apply Blur", command=apply_blur)
        apply_btn.pack(side=tk.LEFT, padx=5)

        return_btn = tk.Button(btn_frame, text="Return to Main", command=return_to_main)
        return_btn.pack(side=tk.RIGHT, padx=5)

    def create_grayscale_view(self):
        if not self.img:
            messagebox.showwarning("Warning", "Please load an image first!")
            return

        # Create grayscale processing tab
        gray_frame = ttk.Frame(self.notebook)
        self.notebook.add(gray_frame, text="Grayscale Processing")

        # Image label for grayscale preview
        gray_image_label = tk.Label(gray_frame)
        gray_image_label.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Buttons frame
        btn_frame = tk.Frame(gray_frame)
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        self.display_image(self.img, gray_image_label)
        # Apply Grayscale Button
        def apply_grayscale():
            grayscale_image = self.processor.apply_grayscale(self.img)

            # Display grayscale image
            self.img = grayscale_image
            self.display_image(self.img, gray_image_label)
            self.display_image(self.img, self.main_image_label)
            # Store processed image
            self.processed_images.append(grayscale_image)

        # Return to Main Button
        def return_to_main():
            # Switch to main tab
            self.notebook.select(0)

            # Remove current tab
            self.notebook.forget(gray_frame)

        # Create buttons
        apply_btn = tk.Button(btn_frame, text="Apply Grayscale", command=apply_grayscale)
        apply_btn.pack(side=tk.LEFT, padx=5)

        return_btn = tk.Button(btn_frame, text="Return to Main", command=return_to_main)
        return_btn.pack(side=tk.RIGHT, padx=5)

    def create_enhance_view(self):
        if not self.img:
            messagebox.showwarning("Warning", "Please load an image first!")
            return

        # Create enhancement processing tab
        enhance_frame = ttk.Frame(self.notebook)
        self.notebook.add(enhance_frame, text="Enhancement Processing")
        self.img_temp = self.img  # Store the original image temporarily
        self.enhanced_img = self.img.copy()  # Start with a copy for updates

        # Main layout frames
        controls_frame = tk.Frame(enhance_frame)
        controls_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        image_frame = tk.Frame(enhance_frame)
        image_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Image label for enhancement preview
        enhance_image_label = tk.Label(image_frame)
        enhance_image_label.pack(expand=True, fill=tk.BOTH)

        # Display the initial image in the enhancement tab
        self.display_image(self.img_temp, enhance_image_label)

        # Real-time update function
        def update_preview(*args):
            brightness = brightness_level.get()
            sharpness = sharpness_level.get()
            contrast = contrast_level.get()
            saturation = saturation_level.get()
            # Apply all enhancements in sequence
            enhanced_img = self.processor.adjust_brightness(self.img_temp, factor=brightness)
            enhanced_img = self.processor.adjust_sharpness(enhanced_img, factor=sharpness)
            enhanced_img = self.processor.adjust_brightness(enhanced_img, factor=contrast)
            enhanced_img = self.processor.adjust_saturation(enhanced_img, factor=saturation)

            self.enhanced_img = enhanced_img  # Store the latest enhanced image
            self.display_image(self.enhanced_img, enhance_image_label)

        # Brightness slider
        tk.Label(controls_frame, text="Brightness Level:").pack(anchor=tk.W, pady=5)
        brightness_level = tk.Scale(
            controls_frame,
            from_=0.0,
            to=10.0,
            resolution=.10,
            orient=tk.HORIZONTAL,
            length=200,
            command=lambda val: update_preview()
        )
        brightness_level.set(1)  # Default value
        brightness_level.pack(anchor=tk.W, pady=5)

        # Sharpness slider
        tk.Label(controls_frame, text="Sharpness Level:").pack(anchor=tk.W, pady=5)
        sharpness_level = tk.Scale(
            controls_frame,
            from_=0.0,
            to=50.0,
            resolution=1.0,
            orient=tk.HORIZONTAL,
            length=200,
            command=lambda val: update_preview()
        )
        sharpness_level.set(1)  # Default value
        sharpness_level.pack(anchor=tk.W, pady=5)

        # Contrast slider
        tk.Label(controls_frame, text="Contrast Level:").pack(anchor=tk.W, pady=5)
        contrast_level = tk.Scale(
            controls_frame,
            from_=0.0,
            to=10.0,
            resolution=.10,
            orient=tk.HORIZONTAL,
            length=200,
            command=lambda val: update_preview()
        )
        contrast_level.set(1)  # Default value
        contrast_level.pack(anchor=tk.W, pady=5)
        #saturation slider
        tk.Label(controls_frame, text="Saturation Level:").pack(anchor=tk.W, pady=5)
        saturation_level = tk.Scale(
            controls_frame,
            from_=0.0,
            to=10.0,
            resolution=.10,
            orient=tk.HORIZONTAL,
            length=200,
            command=lambda val: update_preview()
        )
        saturation_level.set(1)  # Default value
        saturation_level.pack(anchor=tk.W, pady=5)
        # Buttons frame
        btn_frame = tk.Frame(controls_frame)
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        # Save enhancements button
        def save_enhancements():
            self.img = self.enhanced_img.copy()  # Save the enhanced image
            self.display_image(self.img, self.main_image_label)  # Update the main display
            self.processed_images.append(self.img)  # Add to history

        # Return to Main Button
        def return_to_main():
            self.notebook.select(0)
            self.notebook.forget(enhance_frame)

        # Create buttons
        save_btn = tk.Button(btn_frame, text="Save Enhancements", command=save_enhancements)
        save_btn.pack(side=tk.LEFT, padx=5)

        return_btn = tk.Button(btn_frame, text="Return to Main", command=return_to_main)
        return_btn.pack(side=tk.RIGHT, padx=5)
