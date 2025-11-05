import tkinter as tk
from tkinter import ttk
from predict import predict_command

def on_predict():
    command = command_entry.get()
    if command:
        result = predict_command(command)
        result_label.config(text=result)

# Create the main window
root = tk.Tk()
root.title("Command Classifier")
root.geometry("500x250") # Set a default size

# Center the window
window_width = 500
window_height = 250
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')


# Style
style = ttk.Style(root)
style.theme_use("clam")

# Colors
BG_COLOR = "#f0f0f0"
FG_COLOR = "#333333"
BTN_BG_COLOR = "#4a90e2"
BTN_FG_COLOR = "white"

root.configure(bg=BG_COLOR)

# Configure styles
style.configure("TLabel", background=BG_COLOR, foreground=FG_COLOR, font=("Helvetica", 12))
style.configure("TButton", background=BTN_BG_COLOR, foreground=BTN_FG_COLOR, font=("Helvetica", 12, "bold"))
style.map("TButton", background=[("active", "#357abd")])
style.configure("TEntry", font=("Helvetica", 12))


# Create a frame for the content
main_frame = ttk.Frame(root, padding="20")
main_frame.pack(expand=True, fill="both")


# Create and pack the widgets
command_label = ttk.Label(main_frame, text="Enter a command:")
command_label.pack(pady=10)

command_entry = ttk.Entry(main_frame, width=50)
command_entry.pack(pady=5, ipady=5) # Add internal padding

predict_button = ttk.Button(main_frame, text="Predict", command=on_predict, style="TButton")
predict_button.pack(pady=10, ipadx=10, ipady=5) # Add internal padding

result_label = ttk.Label(main_frame, text="", wraplength=450, justify="center")
result_label.pack(pady=10)

# Start the main loop
root.mainloop()