import tkinter as tk
import customtkinter as ctk
import sv_ttk


window = tk.Tk()
window.geometry("400x280")
window.resizable(False, False)
window.title("Password Generator | CodSoft Internship")
window.configure(bg="#2C3E50")


window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)

label = tk.Label(window, text="Password Length", font=("Arial", 14), bg="#2C3E50", fg="white")
label.grid(row=0, column=0, sticky="e", padx=10, pady=20)

entry = tk.Entry(window, width=10)
entry.insert(0, "12")
entry.grid(row=0, column=1, sticky="w", padx=10)

opt1 = tk.IntVar()
opt2 = tk.IntVar()
opt3 = tk.IntVar()

tk.Checkbutton(window, text="Uppercase", variable=opt1, bg="#2C3E50", fg="white").grid(row=1, column=0, pady=5)
tk.Checkbutton(window, text="Numbers", variable=opt2, bg="#2C3E50", fg="white").grid(row=1, column=1, pady=5)
tk.Checkbutton(window, text="Symbols", variable=opt3, bg="#2C3E50", fg="white").grid(row=1, column=2, pady=5)


generate_btn = ctk.CTkButton(
    window, 
    text="Generate Password", 
    corner_radius=20,     # Adjust for roundness
    hover_color="#27ae60", # Color when mouse hovers
    fg_color="#2ecc71",    # Normal button color
    #command=your_function
    font=("Arial", 12, "bold"),
)


#generate_btn = tk.Button(window, text="Generate Password", font=("Arial", 12, "bold"), bg ="#4CAF50", fg="white")
generate_btn.grid(row=2, column=0, columnspan=3, pady=(15,20), padx=20, sticky="ew")
sv_ttk.set_theme("dark")
def toggle_dark_mode():
    window.config(bg="#2d2d2d")
    label.config(bg="#2d2d2d", fg="white")
    # You must manually repeat this for every widget instance

password_val = tk.StringVar(value="P@ssw0rd123!")
output_entry = tk.Entry(
    window,
    textvariable=password_val,
    state="readonly",
    width=30,
    font=("Arial", 10)
)
output_entry.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="we")

copy_btn = tk.Button(window, text="Copy", state="disabled", width=10)
copy_btn.grid(row=3, column=2, padx=10, pady=10)

STRENGHT_COLORS = {
    "Weak": "#FF4B4B",
    "Medium": "#FFA500",
    "Strong": "#2EB82E"
}

strength_label = tk.Label(
    window,
    text="Strenght: -",
    font=("Arial", 10, "bold"),
    justify="center"
)
strength_label.grid(row=4, column=0, columnspan=3, pady=5, sticky="n")

def update_strength(status):
    color = STRENGHT_COLORS.get(status, "black")
    strength_label.config(text=f"Strength: {status}", fg=color)

    if status: 
        copy_btn.config(state="normal")

window.mainloop()
