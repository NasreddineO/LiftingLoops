import tkinter
import customtkinter
import main

# System Settings
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

# App-frame
app = customtkinter.CTk()
app.geometry("600x400")
app.title("LiftingLoops' Protein Folder Deluxe")

# Configure grid
for row in range(4):
    app.grid_rowconfigure(row, weight=(1 if row == 3 else 0))
for col in range(3):
    app.grid_columnconfigure(col, weight=1, uniform="equal")

def checkbox_action(var):
    """
    Funtion that performs a certain action for (un)checked states of checkboxes
    """
    global threeD

    if var == threeD_var:
        threeD = bool(var.get())
    elif var == lookahead_box_var:
        lookahead_entry.grid(row=2, column=1, pady=10, sticky='ew') if var.get() else lookahead_entry.grid_remove()

def on_entry_click(event, entry, placeholder):
    if entry.get() == placeholder:
        entry.delete(0, tkinter.END)
        entry.configure(text_color="white")

def on_focus_out(event, entry, placeholder):
    if not entry.get().strip():
        entry.insert(0, placeholder)
        entry.configure(text_color="gray")

def create_placeholder_entry(row, column, text_var="", placeholder="", master=app, width=100, height=40, columnspan=1, padx=10, pady=10, sticky='ew', show=False):
    """
    Creates a CTkEntry with a placeholder and binds focus events for placeholder functionality.
    """
    entry = customtkinter.CTkEntry(master, width=width, height=height, textvariable=text_var)
    entry.insert(0, placeholder)
    entry.configure(text_color="gray")
    entry.bind("<FocusIn>", lambda event: on_entry_click(event, entry, placeholder))
    entry.bind("<FocusOut>", lambda event: on_focus_out(event, entry, placeholder))
    entry.grid(row=row, column=column, columnspan=columnspan, padx=padx, pady=pady, sticky=sticky)

    if not show:
        entry.grid_remove()

    entry.placeholder = placeholder
    return entry

def update_placeholder(entry, new_placeholder):
    """
    Dynamically updates the placeholder text for an entry and reapplies placeholder behavior.
    """
    if not entry.get().strip() or entry.get() == entry.placeholder:
        entry.delete(0, tkinter.END)
        entry.insert(0, new_placeholder)
        entry.configure(text_color="gray")  # Ensure placeholder styling

    entry.placeholder = new_placeholder  # Update the stored placeholder

    # Reapply bindings for placeholder behavior
    entry.bind("<FocusIn>", lambda event: on_entry_click(event, entry, new_placeholder))
    entry.bind("<FocusOut>", lambda event: on_focus_out(event, entry, new_placeholder))

def update_ui_based_on_algorithm(selected_algorithm):
    """
    Function to update the UI based on selected algorithm
    """
    # Mapping algorithm names to UI components: DONE
    alg_ui_map = {
        "Random": "Number of iterations",
        "Beam Search": "Number of beams",
        "Genetic Algorithm": "Number of parents"
    }

    new_placeholder = alg_ui_map.get(selected_algorithm, "")
    update_placeholder(algorithm_entry, new_placeholder)

    algorithm_entry.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

    if selected_algorithm == "Beam Search":
        beam_lookahead_box.grid(row=2, column=2, pady=10)
    else:
        lookahead_box_var.set(0)
        beam_lookahead_box.grid_remove()
        lookahead_entry.grid_remove()

def handle_error_conditions():
    """
    Handles all the validation logic and shows relevant error messages for each input condition.
    Returns True if any error occurs, otherwise False.
    """
    # Validate protein sequence
    sequence = protein_input.get().strip().upper()
    if sequence == protein_input.placeholder.upper() or not sequence:
        tkinter.messagebox.showerror("Error", "Protein sequence cannot be empty!")
        return True
    if len(sequence) < 2:
        tkinter.messagebox.showerror("Error", "Protein sequence must be longer than 2 amino acids!")
        return True
    if any(char not in "HPC" for char in sequence):
        tkinter.messagebox.showerror("Error", "Protein sequence can only contain 'H', 'P', and 'C'.")
        return True

    # Validate algorithm selection
    if algorithm_var.get() == "Select Algorithm":
        tkinter.messagebox.showerror("Error", "Please select an algorithm.")
        return True

    algorithm_variable = algorithm_specific_var.get()

    # Validate algorithm-specific entry
    if not algorithm_variable or algorithm_variable == algorithm_entry.placeholder:
        tkinter.messagebox.showerror("Error", f"Enter a value for {algorithm_entry.placeholder.lower()}.")
        return True

    if not algorithm_variable.isdigit():
        tkinter.messagebox.showerror("Error", f"Use an integer for {algorithm_entry.placeholder.lower()}.")
        return True

    # Validate lookahead if enabled
    if lookahead_box_var.get():
        lookahead_depth = lookahead_entry.get()
        if not lookahead_depth or lookahead_depth == lookahead_entry.placeholder:
            tkinter.messagebox.showerror("Error", f"Enter a value for {lookahead_entry.placeholder.lower()}.")
            return True

        if not lookahead_depth.isdigit():
            tkinter.messagebox.showerror("Error", f"Use an integer for {lookahead_entry.placeholder.lower()}.")
            return True

    return False

def fold_protein():
    """
    Handles the protein folding process, validates inputs, and manages algorithm settings.
    """
    # Call the error handling function
    if handle_error_conditions():
        return

    # If all validations pass, proceed
    sequence = protein_input.get().strip().upper()
    algorithm = algorithm_var.get()
    algorithm_variable = algorithm_specific_var.get()
    lookahead_depth = lookahead_entry.get()

    if not lookahead_box_var.get():
        print(f"3D: {threeD}, Sequence: {sequence}, Algorithm: {algorithm}, Variable: {algorithm_variable}")
    else:
        print(f"3D: {threeD}, Sequence: {sequence}, Algorithm: {algorithm}, Variable: {algorithm_variable}, Lookahead depth: {lookahead_depth}")

# Protein sequence input
p_sequence = tkinter.StringVar()
protein_input = create_placeholder_entry(text_var=p_sequence, placeholder="Insert a protein sequence", row=0, column=0, columnspan=5, show=True)

# Checkbox for 2D/3D option
threeD_var = customtkinter.IntVar()
threeD = False
threeD_checkbox = customtkinter.CTkCheckBox(app, text="Enable 3D", variable=threeD_var, command=lambda: checkbox_action(threeD_var))
threeD_checkbox.grid(row=1, column=0, pady=10)

# Checkbox and entrybox for Lookahead
lookahead_box_var = customtkinter.IntVar()
lookahead_var = customtkinter.StringVar()
beam_lookahead_box = customtkinter.CTkCheckBox(app, text="Enable lookahead", variable=lookahead_box_var, command=lambda: checkbox_action(lookahead_box_var))
lookahead_entry = create_placeholder_entry(2, 1, text_var=lookahead_var, placeholder="Lookahead depth")

# Algorithm specific entrybox based on algorithm selection
algorithm_specific_var = customtkinter.StringVar()
algorithm_entry = create_placeholder_entry(2, 0, text_var=algorithm_specific_var, placeholder="")

# Dropdown menu for algorithm selection
algorithm_options = ["Random", "Random Greedy", "Beam Search", "Genetic Algorithm"]
algorithm_var = customtkinter.StringVar(value="Select Algorithm")
algorithm_menu = customtkinter.CTkOptionMenu(app, variable=algorithm_var, values=algorithm_options, command=update_ui_based_on_algorithm)
algorithm_menu.grid(row=1, column=2, pady=10)

# Run button
run = customtkinter.CTkButton(app, text="Fold protein", command=fold_protein)
run.grid(row=10, column=0, padx=10, pady=10, columnspan=2)

# Run app
app.mainloop()
