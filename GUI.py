import tkinter as tk
from tkinter import filedialog
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageOps, ImageFilter
import sqlite3

# Database setup
DATABASE = "images.db"

def init_database():
    """Initialize the SQLite database and create the table if it doesn't exist."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_image_to_database(file_path):
    """Save the image file path to the database."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO images (file_path) VALUES (?)", (file_path,))
    conn.commit()
    conn.close()

def fetch_images_from_database():
    """Fetch all image file paths from the database."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT file_path FROM images")
    images = cursor.fetchall()
    conn.close()
    return [image[0] for image in images]

def browse_image(label_original, label_processed):
    """Browse and display an image, and save it to the database."""
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg *.bmp")])
    if file_path:
        original_image = Image.open(file_path)
        original_image.thumbnail((300, 300))
        original_photo = ImageTk.PhotoImage(original_image)
        label_original.image = original_photo
        label_original.config(image=original_photo)
        label_processed.image = None
        label_processed.config(image=None)  # Clear processed image
        save_image_to_database(file_path)  # Save to database
        return original_image
    return None

def load_image_from_database(label_original, label_processed):
    """Load an image from the database and display it."""
    images = fetch_images_from_database()
    if not images:
        messagebox.showinfo("No Images", "No images found in the database.")
        return None
    # Select the first image in the database (or customize the selection logic)
    file_path = images[-1]
    original_image = Image.open(file_path)
    original_image.thumbnail((300, 300))
    original_photo = ImageTk.PhotoImage(original_image)
    label_original.image = original_photo
    label_original.config(image=original_photo)
    label_processed.image = None
    label_processed.config(image=None)  # Clear processed image
    return original_image

def remove_noise(image):
    if image:
        return image.filter(ImageFilter.MedianFilter(size=3))
    return None

def apply_histogram_equalization(image):
    if image:
        return ImageOps.equalize(image.convert("RGB"))
    return None

def process_image(image, process_function, label_processed):
    """Process the image using the specified function and update the processed label."""
    if image:
        processed_image = process_function(image)
        if processed_image:
            processed_image.thumbnail((300, 300))
            processed_photo = ImageTk.PhotoImage(processed_image)
            label_processed.image = processed_photo
            label_processed.config(image=processed_photo)
        return processed_image
    return None

def create_main_page(root):
    """Create the main page."""
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Image Processing App - Main Page")

    # frame = ttk.Frame(root, padding="10")
    # frame.pack(fill="both", expand=True)

    label = ttk.Label(root, text="Welcome to Image Processing App!", font=("Helvetica", 18))
    label.pack(pady=20)

    button_restore = ttk.Button(root, text="Restore Image", command=lambda: create_restore_page(root))
    button_restore.pack(pady=10, ipadx=20)

    button_histogram = ttk.Button(root, text="Histogram Equalization", command=lambda: create_histogram_page(root))
    button_histogram.pack(pady=10, ipadx=20)

    exit_button = ttk.Button(root, text="Exit", command=root.quit)
    exit_button.pack(pady=20)

def create_restore_page(root):
    """Create the restore image page."""
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Restore Image")

    # frame = ttk.Frame(root, padding="10")
    # frame.pack(fill="both", expand=True)

    ttk.Label(root, text="Original Image", font=("Helvetica", 14)).pack(pady=5)
    label_original = ttk.Label(root)
    label_original.pack(pady=5)

    ttk.Label(root, text="Processed Image", font=("Helvetica", 14)).pack(pady=5)
    label_processed = ttk.Label(root)
    label_processed.pack(pady=5)

    state = {"original_image": None}

    browse_button = ttk.Button(
        root,
        text="Browse Image",
        command=lambda: state.update(original_image=browse_image(label_original, label_processed)),
    )
    browse_button.pack(pady=10)

    load_db_button = ttk.Button(
        root,
        text="Load from Database",
        command=lambda: state.update(original_image=load_image_from_database(label_original, label_processed)),
    )
    load_db_button.pack(pady=10)

    remove_noise_button = ttk.Button(
        root,
        text="Remove Noise",
        command=lambda: process_image(state.get("original_image"), remove_noise, label_processed),
    )
    remove_noise_button.pack(pady=10)

    main_menu_button = ttk.Button(root, text="Main Menu", command=lambda: create_main_page(root))
    main_menu_button.pack(side="left", padx=20, pady=20)

    exit_button = ttk.Button(root, text="Exit", command=root.quit)
    exit_button.pack(side="right", padx=20, pady=20)

def create_histogram_page(root):
    """Create the histogram equalization page."""
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Histogram Equalization")

    # frame = ttk.Frame(root, padding="10")
    # frame.pack(fill="both", expand=True)

    ttk.Label(root, text="Original Image", font=("Helvetica", 14)).pack(pady=5)
    label_original = ttk.Label(root)
    label_original.pack(pady=5)

    ttk.Label(root, text="Equalized Image", font=("Helvetica", 14)).pack(pady=5)
    label_processed = ttk.Label(root)
    label_processed.pack(pady=5)

    state = {"original_image": None}

    browse_button = ttk.Button(
        root,
        text="Browse Image",
        command=lambda: state.update(original_image=browse_image(label_original, label_processed)),
    )
    browse_button.pack(pady=10)

    load_db_button = ttk.Button(
        root,
        text="Load from Database",
        command=lambda: state.update(original_image=load_image_from_database(label_original, label_processed)),
    )
    load_db_button.pack(pady=10)

    equalize_button = ttk.Button(
        root,
        text="Equalize Histogram",
        command=lambda: process_image(state.get("original_image"), apply_histogram_equalization, label_processed),
    )
    equalize_button.pack(pady=10)

    main_menu_button = ttk.Button(root, text="Main Menu", command=lambda: create_main_page(root))
    main_menu_button.pack(side="left", padx=20, pady=20)

    exit_button = ttk.Button(root, text="Exit", command=root.quit)
    exit_button.pack(side="right", padx=20, pady=20)

def main():
    window = tk.Tk()
    window.attributes('-fullscreen', True)
    window.style = ttk.Style()
    window.style.theme_use("clam")

    create_main_page(window)

    window.mainloop()

if __name__ == "__main__":
    main()


