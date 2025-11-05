
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

# Create and pack the widgets
command_label = ttk.Label(root, text="Enter a command:")
command_label.pack(pady=5)

command_entry = ttk.Entry(root, width=50)
command_entry.pack(pady=5)

predict_button = ttk.Button(root, text="Predict", command=on_predict)
predict_button.pack(pady=5)

result_label = ttk.Label(root, text="")
result_label.pack(pady=5)

# Start the main loop
root.mainloop()
