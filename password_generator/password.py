import tkinter as tk
import customtkinter as ctk
import sv_ttk


window = tk.Tk()
window.geometry("400x280")
window.resizable(False, False)
window.title("Password Generator | CodSoft Internship")
window.configure(bg="#1e1e2e")


window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)

label = tk.Label(window, text="Password Length", font=("Segoe UI", 12, "bold"), bg="#1e1e2e", fg="#cdd6f4")
label.grid(row=0, column=0, sticky="e", padx=(5, 10), pady=(20, 10))

entry = tk.Entry(window, width=8, font=("Segoe UI", 11), justify="center", bg="#313244", fg="#cdd6f4", relief="flat", highlightthickness=1, highlightbackground="#45475a")
entry.insert(0, "12")
entry.grid(row=0, column=1, sticky="w", padx=10)

opt1 = tk.IntVar(value=1)
opt2 = tk.IntVar(value=1)
opt3 = tk.IntVar(value=1)

cb_frame = tk.Frame(window, bg="#1e1e2e")
cb_frame.grid(row=1, column=0, columnspan=3, pady=5)

cb1 = ctk.CTkCheckBox(cb_frame, text="Uppercase (A-Z)", variable=opt1, font=("Segoe UI", 10), fg_color="#27ae60", border_color="#45475a", hover_color="#006400")
cb1.pack(side="left", padx=8)

cb2 = ctk.CTkCheckBox(cb_frame, text="Numbers (0-9)", variable=opt2, font=("Segoe UI", 10), fg_color="#27ae60", border_color="#45475a", hover_color="#006400")
cb2.pack(side="left", padx=8)

cb3 = ctk.CTkCheckBox(cb_frame, text="Symbols (!@#)", variable=opt3, font=("Segoe UI", 10), fg_color="#27ae60", border_color="#45475a", hover_color="#006400")
cb3.pack(side="left", padx=8)

generate_btn = ctk.CTkButton(
    window, 
    text="Generate Password", 
    corner_radius=15,
    # hover_color="#27ae60",
    # fg_color="#89b4fa",
    hover_color="#008000",
    fg_color="#27ae60",
    font=("Segoe UI", 11, "bold"),
    text_color="#1e1e2e",
    height=35
)
generate_btn.grid(row=2, column=0, columnspan=3, pady=(15, 15), padx=30, sticky="ew")

sv_ttk.set_theme("dark")

password_val = tk.StringVar(value="")
output_frame = tk.Frame(window, bg="#1e1e2e")
output_frame.grid(row=3, column=0, columnspan=3, padx=15, pady=(5, 10), sticky="ew")
output_frame.grid_columnconfigure(0, weight=1)

output_entry = tk.Entry(
    output_frame,
    textvariable=password_val,
    state="readonly",
    width=25,
    font=("Consolas", 11),
    bg="#313244",
    fg="#a6e3a1",
    relief="flat",
    readonlybackground="#313244"
)
output_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))

copy_btn = tk.Button(output_frame, text="Copy", font=("Segoe UI", 9, "bold"), width=8, bg="#45475a", fg="#cdd6f4", relief="flat", state="disabled")
copy_btn.grid(row=0, column=1)

STRENGTH_COLORS = {
    "Weak": "#f38ba8",
    "Medium": "#fab387",
    "Strong": "#a6e3a1"
}

strength_label = tk.Label(
    window,
    text="Strength: -",
    font=("Segoe UI", 10, "bold"),
    bg="#1e1e2e",
    fg="#6c7086",
    justify="center"
)
strength_label.grid(row=4, column=0, columnspan=3, pady=(5, 15), sticky="n")

def update_strength(status):
    color = STRENGTH_COLORS.get(status, "#6c7086")
    strength_label.config(text=f"Strength: {status}", fg=color)
    if status: 
        copy_btn.config(state="normal", bg="#3179ca")

def generate_password():
    import random
    import string
    
    length = int(entry.get()) if entry.get().isdigit() else 12
    chars = string.ascii_lowercase
    
    if opt1.get():
        chars += string.ascii_uppercase
    if opt2.get():
        chars += string.digits
    if opt3.get():
        chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    if not opt1.get() and not opt2.get() and not opt3.get():
        chars += string.ascii_uppercase + string.digits
    
    password = ''.join(random.choice(chars) for _ in range(length))
    password_val.set(password)
    
    if len(password) < 8:
        update_strength("Weak")
    elif len(password) < 16:
        update_strength("Medium")
    else:
        update_strength("Strong")

def copy_password():
    import pyperclip
    pyperclip.copy(password_val.get())

generate_btn.configure(command=generate_password)
copy_btn.configure(command=copy_password)

window.mainloop()
