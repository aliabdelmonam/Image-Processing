import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
from Image_processing_Project import ImageProcessor  # Import from first file
from tkinter import colorchooser


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
        self.padd_color = (0,0,0)
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
            # ("Blur", self.create_blur_view),
            ("Grayscale", self.create_grayscale_view),
            ("Enhance", self.create_enhance_view),
            ("Equalization",self.create_hist_label),
            ("Padding",self.create_padd_tab),
            ("Noise Removal",self.create_noise_removal),
            ("Transformation",self.transormation),
            ("Reset", self.create_reset_button),
            ("Save",self.save_image_to_disk)
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

########################################################################################################################
    def create_reset_button(self):
        if not self.img:
            messagebox.showwarning("Warning", "No image to reset!")
            return
        # Create a Reset button and add it to the UI

        self.img = self.original_image
        self.display_image(self.img, self.main_image_label)

########################################################################################################################
    # def create_blur_view(self):
    #     if not self.img:
    #         messagebox.showwarning("Warning", "Please load an image first!")
    #         return
    #
    #     # Create blur processing tab
    #     blur_frame = ttk.Frame(self.notebook)
    #     self.notebook.add(blur_frame, text="Blur Processing")
    #
    #     # Blur intensity slider
    #     slider_frame = tk.Frame(blur_frame)
    #     slider_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
    #
    #     tk.Label(slider_frame, text="Blur Intensity:").pack(side=tk.LEFT)
    #     blur_intensity = tk.Scale(
    #         slider_frame,
    #         from_=0,
    #         to=10,
    #         orient=tk.HORIZONTAL,
    #         length=300
    #     )
    #     blur_intensity.pack(side=tk.LEFT, expand=True, fill=tk.X)
    #
    #     # Image label for blur preview
    #     blur_image_label = tk.Label(blur_frame)
    #     blur_image_label.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
    #
    #     # Buttons frame
    #     btn_frame = tk.Frame(blur_frame)
    #     btn_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
    #
    #     # Apply Blur Button
    #     self.display_image(self.img, blur_image_label)
    #     def apply_blur():
    #         intensity = blur_intensity.get()
    #         blurred_image = self.processor.apply_blur(
    #             self.img,
    #             radius=intensity
    #         )
    #         self.img = blurred_image
    #         # Display blurred image
    #         self.display_image(self.img, blur_image_label)
    #         self.display_image(self.img, self.main_image_label)
    #         # Store processed image
    #         self.processed_images.append(blurred_image)
    #
    #     # Return to Main Button
    #     def return_to_main():
    #         # Switch to main tab
    #         self.notebook.select(0)
    #
    #         # Remove current tab
    #         self.notebook.forget(blur_frame)
    #
    #     # Create buttons
    #     apply_btn = tk.Button(btn_frame, text="Apply Blur", command=apply_blur)
    #     apply_btn.pack(side=tk.LEFT, padx=5)
    #
    #     return_btn = tk.Button(btn_frame, text="Return to Main", command=return_to_main)
    #     return_btn.pack(side=tk.RIGHT, padx=5)

########################################################################################################################
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
        self.img_temp = self.img
        self.enhanced_img = self.img.copy()
        # Apply Grayscale Button
        def apply_grayscale():
            grayscale_image = self.processor.apply_grayscale(self.img_temp)
            self.enhanced_img = grayscale_image
            self.display_image(grayscale_image, gray_image_label)
            # Store processed image

        # Return to Main Button
        def return_to_main():
            # Switch to main tab
            self.notebook.select(0)

            # Remove current tab
            self.notebook.forget(gray_frame)
        def save_enhancements():
            self.img = self.enhanced_img.copy()
            self.display_image(self.img, self.main_image_label)

        save_btn = tk.Button(btn_frame, text="Save Enhancements", command=save_enhancements)
        save_btn.pack(side=tk.LEFT, padx=5, pady=5)

        # Create buttons
        apply_btn = tk.Button(btn_frame, text="Apply Grayscale", command=apply_grayscale)
        apply_btn.pack(side=tk.LEFT, padx=5)

        return_btn = tk.Button(btn_frame, text="Return to Main", command=return_to_main)
        return_btn.pack(side=tk.RIGHT, padx=5)

########################################################################################################################
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
        controls_frame.pack(side=tk.LEFT, fill=tk.Y, padx=15, pady=10)

        image_frame = tk.Frame(enhance_frame)
        image_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=15, pady=10)

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

        # Control labels and sliders (Using pack for consistent layout)
        tk.Label(controls_frame, text="Brightness Level:").pack(anchor=tk.W, pady=5)
        brightness_level = tk.Scale(
            controls_frame,
            from_=0.0,
            to=10.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            length=200,
            command=lambda val: update_preview()
        )
        brightness_level.set(1)  # Default value
        brightness_level.pack(anchor=tk.W, pady=5)

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

        tk.Label(controls_frame, text="Contrast Level:").pack(anchor=tk.W, pady=5)
        contrast_level = tk.Scale(
            controls_frame,
            from_=0.0,
            to=10.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            length=200,
            command=lambda val: update_preview()
        )
        contrast_level.set(1)  # Default value
        contrast_level.pack(anchor=tk.W, pady=5)

        tk.Label(controls_frame, text="Saturation Level:").pack(anchor=tk.W, pady=5)
        saturation_level = tk.Scale(
            controls_frame,
            from_=0.0,
            to=10.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            length=200,
            command=lambda val: update_preview()
        )
        saturation_level.set(1)  # Default value
        saturation_level.pack(anchor=tk.W, pady=5)

        # Buttons Frame at the bottom
        btn_frame = tk.Frame(controls_frame)
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=15)

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
        save_btn.pack(side=tk.LEFT, padx=10)

        return_btn = tk.Button(btn_frame, text="Return to Main", command=return_to_main)
        return_btn.pack(side=tk.RIGHT, padx=10)

########################################################################################################################
    def create_hist_label (self):
        if not self.img:
            messagebox.showwarning("Warning", "Please load an image first!")
            return
        OPX_frame = ttk.Frame(self.notebook)
        self.notebook.add(OPX_frame, text="OPX Processing")

        # Image label for grayscale preview
        OPX_image_label = tk.Label(OPX_frame)
        OPX_image_label.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Buttons frame
        btn_frame = tk.Frame(OPX_frame)
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        self.display_image(self.img, OPX_image_label)
        self.temp = self.img
        def apply_hist():
            hist_image = self.processor.apply_hist_equalization(self.temp)
            self.temp = hist_image
            self.display_image(self.temp,OPX_image_label)

        def return_to_main():
            # Switch to main tab
            self.notebook.select(0)

            # Remove current tab
            self.notebook.forget(OPX_frame)
        def save_update():
            self.img = self.temp
            self.display_image(self.img,self.main_image_label)
            self.processed_images.append(self.img)
        # Create buttons
        apply_btn = tk.Button(btn_frame, text="Apply Histogram Equalization", command=apply_hist)
        apply_btn.pack(side=tk.LEFT, padx=5)

        apply_btn = tk.Button(btn_frame, text="Save Update", command=save_update)
        apply_btn.pack(side=tk.LEFT, padx=5)

        return_btn = tk.Button(btn_frame, text="Return to Main", command=return_to_main)
        return_btn.pack(side=tk.RIGHT, padx=5)

########################################################################################################################
    def create_padd_tab(self):
        if not self.img:
            messagebox.showwarning("Warning", "Please load an image first!")
            return
        padd_frame = ttk.Frame(self.notebook)
        self.notebook.add(padd_frame, text="Adding Padding")

        # Top frame for controls (Spinbox, Label, Checkboxes)
        top_frame = tk.Frame(padd_frame)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Label and Spinbox for Padding Thickness
        tk.Label(top_frame, text="Padding Thickness:").pack(side=tk.LEFT, padx=5)

        thickness_var = tk.StringVar(value='0')
        thickness_spinner = tk.Spinbox(
            top_frame,
            from_=0,
            to=1000,
            increment=1,
            width=5,
            textvariable=thickness_var
        )
        thickness_spinner.pack(side=tk.LEFT, padx=5)

        # Check Buttons frame inside the top frame
        check_frame = tk.Frame(top_frame)
        check_frame.pack(side=tk.LEFT, padx=20)

        tk.Label(check_frame, text='Position', font="Arial 12 bold").pack(anchor=tk.W)

        # Check Vars
        check_vars = {
            "down": tk.IntVar(),
            "up": tk.IntVar(),
            "left": tk.IntVar(),
            "right": tk.IntVar()
        }

        # Position checkboxes
        button_positions = [
            ("DOWN", "down"),
            ("UP", "up"),
            ("LEFT", "left"),
            ("RIGHT", "right")
        ]
        for text, key in button_positions:
            tk.Checkbutton(
                check_frame,
                text=text,
                variable=check_vars[key],
                command=lambda: update_preview()
            ).pack(anchor=tk.W)

        # Image label for preview (centered, large space)
        padd_image_label = tk.Label(padd_frame)
        padd_image_label.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Bottom frame for buttons
        btn_frame = tk.Frame(padd_frame)
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        self.display_image(self.img, padd_image_label)
        self.img_temp = self.img
        self.enhanced_img = self.img.copy()
        self.padd_color = (0, 0, 0)  # Default black color

        # Function to update the preview
        def update_preview(*args):
            try:
                thickness = int(thickness_var.get())
            except ValueError:
                thickness = 0

            color = self.padd_color
            left = thickness if check_vars["left"].get() == 1 else 0
            right = thickness if check_vars["right"].get() == 1 else 0
            top = thickness if check_vars["up"].get() == 1 else 0
            bottom = thickness if check_vars["down"].get() == 1 else 0

            enhanced_img = self.processor.apply_padding(
                self.img_temp, left, top, right, bottom, fill=color
            )
            self.enhanced_img = enhanced_img
            self.display_image(self.enhanced_img, padd_image_label)

        # Add trace to thickness variable
        thickness_var.trace_add('write', update_preview)

        # Color selection button
        def choose_color():
            color_code = colorchooser.askcolor(title="Choose color")[0]
            if color_code:
                self.padd_color = color_code
                update_preview()

        choose_button = tk.Button(btn_frame, text="Choose Color", command=choose_color)
        choose_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Save Enhancements button
        def save_enhancements():
            self.img = self.enhanced_img.copy()
            self.display_image(self.img, self.main_image_label)

        save_btn = tk.Button(btn_frame, text="Save Enhancements", command=save_enhancements)
        save_btn.pack(side=tk.LEFT, padx=5, pady=5)

        # Return to Main button
        def return_to_main():
            self.notebook.select(0)
            self.notebook.forget(padd_frame)

        return_btn = tk.Button(btn_frame, text="Return to Main", command=return_to_main)
        return_btn.pack(side=tk.RIGHT, padx=5, pady=5)

########################################################################################################################
    def create_noise_removal(self):

        if not self.img:
            messagebox.showwarning("Warning", "Please load an image first!")
            return

        Noise_frame = ttk.Frame(self.notebook)
        self.notebook.add(Noise_frame, text="Remove Noise")

        # Create top frame for kernel size selections
        top_frame = tk.Frame(Noise_frame)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Gaussian Blur Controls
        tk.Label(top_frame, text="Gaussian Kernel Size:").pack(side=tk.LEFT, padx=5)
        gas_kernel_var = tk.StringVar(value='1')
        gas_kernel = tk.Spinbox(
            top_frame,
            from_=1,
            to=101,
            increment=2,
            width=5,
            textvariable=gas_kernel_var
        )
        gas_kernel.pack(side=tk.LEFT, pady=10)

        # Median Filter Controls
        tk.Label(top_frame, text="Median Kernel Size:").pack(side=tk.LEFT, padx=5)
        med_kernel_var = tk.StringVar(value='1')
        med_kernel = tk.Spinbox(
            top_frame,
            from_=1,
            to=21,
            increment=2,
            width=5,
            textvariable=med_kernel_var
        )
        med_kernel.pack(side=tk.LEFT, pady=10)

        # Bilateral Filter Controls
        tk.Label(top_frame, text="Bilateral Sigma Color:").pack(side=tk.LEFT, padx=5)
        bie_color_kernel_var = tk.StringVar(value='1')
        bie_color_kernel = tk.Spinbox(
            top_frame,
            from_=1,
            to=151,
            increment=2,
            width=5,
            textvariable=bie_color_kernel_var
        )
        bie_color_kernel.pack(side=tk.LEFT, pady=10)

        tk.Label(top_frame, text="Bilateral Sigma Space:").pack(side=tk.LEFT, padx=5)
        bie_space_kernel_var = tk.StringVar(value='1')
        bie_space_kernel = tk.Spinbox(
            top_frame,
            from_=1,
            to=151,
            increment=2,
            width=5,
            textvariable=bie_space_kernel_var
        )
        bie_space_kernel.pack(side=tk.LEFT, pady=10)

        tk.Label(top_frame, text="Bilateral D:").pack(side=tk.LEFT, padx=5)
        bie_d_kernel_var = tk.StringVar(value='1')
        bie_d_kernel = tk.Spinbox(
            top_frame,
            from_=1,
            to=151,
            increment=2,
            width=5,
            textvariable=bie_d_kernel_var
        )
        bie_d_kernel.pack(side=tk.LEFT, pady=10)

        # Image display label
        noise_image_label = tk.Label(Noise_frame)
        noise_image_label.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Button frame
        btn_frame = tk.Frame(Noise_frame)
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        # Initial image setup
        self.display_image(self.img, noise_image_label)
        self.img_temp = self.img
        self.enhanced_img = self.img.copy()

        # Noise removal method checkboxes
        noise_removal_frame = tk.Frame(Noise_frame)
        noise_removal_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Checkbox variables
        gaussian_var = tk.BooleanVar(value=False)
        median_var = tk.BooleanVar(value=False)
        bilateral_var = tk.BooleanVar(value=False)

        # Create checkboxes for each noise removal method
        gaussian_check = tk.Checkbutton(
            noise_removal_frame,
            text="Gaussian Blur",
            variable=gaussian_var,
            command=lambda: update_preview()
        )
        gaussian_check.pack(side=tk.LEFT, padx=5)

        median_check = tk.Checkbutton(
            noise_removal_frame,
            text="Median Filter",
            variable=median_var,
            command=lambda: update_preview()
        )
        median_check.pack(side=tk.LEFT, padx=5)

        bilateral_check = tk.Checkbutton(
            noise_removal_frame,
            text="Bilateral Filter",
            variable=bilateral_var,
            command=lambda: update_preview()
        )
        bilateral_check.pack(side=tk.LEFT, padx=5)

        def update_preview():
            # Start with the original image
            enhanced_img = self.img_temp.copy()

            # Apply Gaussian Blur if checked
            if gaussian_var.get():
                try:
                    gauassian_kernel = int(gas_kernel_var.get())
                    enhanced_img = self.processor.apply_blur(enhanced_img, radius=gauassian_kernel)
                except ValueError:
                    print("Invalid Gaussian kernel size")

            # Apply Median Filter if checked
            if median_var.get():
                try:
                    median_kernel = int(med_kernel_var.get())
                    enhanced_img = self.processor.apply_median_filter(enhanced_img, size=median_kernel)
                except ValueError:
                    print("Invalid Median kernel size")

            # Apply Bilateral Filter if checked
            if bilateral_var.get():
                try:
                    sigma_color = int(bie_color_kernel_var.get())
                    sigma_space = int(bie_space_kernel_var.get())
                    d           = int(bie_d_kernel_var.get())
                    enhanced_img = self.processor.apply_bilateral_filter(
                        enhanced_img,
                        d=d,
                        sigmacolor=sigma_color,
                        sigmaspace=sigma_space
                    )
                except ValueError:
                    print("Invalid Bilateral filter parameters")

            # Update the displayed image and store the enhanced version
            self.enhanced_img = enhanced_img
            self.display_image(self.enhanced_img, noise_image_label)

        # Trace variables to update preview when kernel sizes change
        gas_kernel_var.trace_add('write', lambda *args: update_preview())
        med_kernel_var.trace_add('write', lambda *args: update_preview())
        bie_space_kernel_var.trace_add('write', lambda *args: update_preview())
        bie_color_kernel_var.trace_add('write', lambda *args: update_preview())

        def save_enhancements():
            self.img = self.enhanced_img.copy()
            self.display_image(self.img, self.main_image_label)

        save_btn = tk.Button(btn_frame, text="Save Enhancements", command=save_enhancements)
        save_btn.pack(side=tk.LEFT, padx=5, pady=5)

        def return_to_main():
            self.notebook.select(0)
            self.notebook.forget(Noise_frame)

        return_btn = tk.Button(btn_frame, text="Return to Main", command=return_to_main)
        return_btn.pack(side=tk.RIGHT, padx=5, pady=5)

########################################################################################################################
    def transormation(self):
        if not self.img:
            messagebox.showwarning("Warning", "Please load an image first!")
            return
        transform_frame = ttk.Frame(self.notebook)
        self.notebook.add(transform_frame, text="Transformation")

        top_frame = tk.Frame(transform_frame)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Gaussian Blur Controls
        tk.Label(top_frame, text="Angle:").pack(side=tk.LEFT, padx=5)
        angle_spinner_var = tk.StringVar(value='0')
        angle_spinner = tk.Spinbox(
            top_frame,
            from_=0,
            to=360,
            increment=2,
            width=5,
            textvariable=angle_spinner_var
        )
        angle_spinner.pack(side=tk.LEFT, pady=10)

        tk.Label(top_frame, text="Scale:").pack(side=tk.LEFT, padx=5)
        scale_spinner_var = tk.StringVar(value='1')
        scale_spinner = tk.Spinbox(
            top_frame,
            from_=1,
            to=10,
            increment=1,
            width=5,
            textvariable=scale_spinner_var
        )
        scale_spinner.pack(side=tk.LEFT, pady=10)

        transform_image_label = tk.Label(transform_frame)
        transform_image_label.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Button frame
        btn_frame = tk.Frame(transform_frame)
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        # Initial image setup
        self.display_image(self.img, transform_image_label)
        self.img_temp = self.img
        self.enhanced_img = self.img.copy()


        def update_preview():
            try:
                angle= int(angle_spinner_var.get())
                scale= int(scale_spinner_var.get())
                enhanced_img = self.processor.apply_transformation(self.img_temp,angle=angle,scale=scale)
            except ValueError:
                # messagebox.showwarning("Warning", "Invalid Values for transformation!")
                print("Invalid Values for transformation!")
            self.enhanced_img = enhanced_img
            self.display_image(self.enhanced_img, transform_image_label)

        scale_spinner_var.trace_add('write', lambda *args: update_preview())
        angle_spinner_var.trace_add('write', lambda *args: update_preview())

        def save_enhancements():
            self.img = self.enhanced_img.copy()
            self.display_image(self.img, self.main_image_label)

        save_btn = tk.Button(btn_frame, text="Save Enhancements", command=save_enhancements)
        save_btn.pack(side=tk.LEFT, padx=5, pady=5)

        def return_to_main():
            self.notebook.select(0)
            self.notebook.forget(transform_frame)

        return_btn = tk.Button(btn_frame, text="Return to Main", command=return_to_main)
        return_btn.pack(side=tk.RIGHT, padx=5, pady=5)

########################################################################################################################
    def save_image_to_disk(self):
        # Open a file dialog to get the save location
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg"),
                                                            ("All Files", "*.*")])

        if file_path:  # If user selects a file path
            try:
                self.img.save(file_path)  # Save the image
                messagebox.showinfo("Save Image", f"Image saved successfully to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image. Error: {e}")