import tkinter as tk
from GUI import ImageProcessingApp

def main():
    """
    Main function to launch the application.
    """
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()