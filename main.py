from classes import *
from database_manager import *
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

# Global variables
current_object = None
current_edit_id = None
action_history = []

def setup_ui(root):
    # Main frames
    lists_frame = ttk.Frame(root, padding="10")
    lists_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    info_frame = ttk.Frame(root, padding="10")
    info_frame.pack(side=tk.LEFT, fill=tk.Y)
    
    history_frame = ttk.Frame(root, padding="10")
    history_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    # Lists frame
    for art_type in ['Painting', 'Sculpture']:
        ttk.Label(lists_frame, text=f"{art_type}s:").pack(anchor=tk.W)
        listbox = tk.Listbox(lists_frame, height=10, width=60)
        listbox.pack(fill=tk.X, padx=5, pady=5)
        globals()[f"{art_type.lower()}s_list"] = listbox
        listbox.bind('<<ListboxSelect>>', lambda e, t=art_type.lower(): on_art_select(t))
    
    buttons = [
        ("Delete", delete_selected),
        ("Update", edit_selected),
        ("Create Painting", lambda: show_edit_dialog('painting')),
        ("Create Sculpture", lambda: show_edit_dialog('sculpture')),
        ("Refresh Lists", refresh_lists)
    ]
    
    for text, cmd in buttons:
        ttk.Button(lists_frame, text=text, command=cmd).pack(side=tk.LEFT, padx=2, pady=5)
    
    # Info frame
    ttk.Label(info_frame, text="Selected Object:").pack(anchor=tk.W)
    global selected_obj_label
    selected_obj_label = ttk.Label(info_frame, text="None", wraplength=200)
    selected_obj_label.pack(anchor=tk.W, pady=5)
    
    ttk.Label(info_frame, text="Actions:").pack(anchor=tk.W, pady=(10, 0))
    global action_buttons_frame
    action_buttons_frame = ttk.Frame(info_frame)
    action_buttons_frame.pack(fill=tk.X)
    
    # History frame
    ttk.Label(history_frame, text="Action History:").pack(anchor=tk.W)
    global history_text
    history_text = scrolledtext.ScrolledText(history_frame, width=40, height=20, wrap=tk.WORD)
    history_text.pack(fill=tk.BOTH, expand=True)
    history_text.config(state=tk.DISABLED)
    ttk.Button(history_frame, text="Clear History", 
              command=lambda: [globals().__setitem__('action_history', []), update_history()]).pack(pady=5)

def update_history():
    history_text.config(state=tk.NORMAL)
    history_text.delete(1.0, tk.END)
    history_text.insert(tk.END, "\n".join(action_history))
    history_text.see(tk.END)
    history_text.config(state=tk.DISABLED)

def on_art_select(art_type):
    global current_object
    listbox = globals()[f"{art_type}s_list"]
    if not listbox.curselection(): 
        return

    item = listbox.get(listbox.curselection()[0])
    art_id = int(item.split('|')[0].split(':')[1].strip())
    data = read(art_type, art_id)

    messagebox.showwarning("Warning", data[0] + " " + data[1] + " " + data[3])
    
    if not data:
        return

    if art_type == 'painting':
        current_object = Painting(
            title=data[0],
            author=data[1],
            size=data[2],
            type_color=data[3]
        )
    else:
        current_object = Sculpture(
            title=data[0],   # title
            author=data[1],  # author
            weight=data[2],  # weight
            material=data[3] # material
        )

    # Update interface
    selected_obj_label.config(
        text=f"{art_type.capitalize()}:\n{current_object.get_title()}\nby {current_object.get_author()}"
    )
    add_to_history(f"Selected {art_type}: {current_object.get_title()} by {current_object.get_author()}")

def refresh_lists():
    for art_type in ['painting', 'sculpture']:
        listbox = globals()[f"{art_type}s_list"]
        listbox.delete(0, tk.END)
        items = get_all_paintings() if art_type == 'painting' else get_all_sculptures()
        
        for item in items:
            listbox.insert(tk.END, 
                f"ID: {item[0]} | {item[1]} by {item[2]} | {'Size' if art_type == 'painting' else 'Weight'}: {item[3]} | {'Type' if art_type == 'painting' else 'Material'}: {item[4]}")

def delete_selected():
    global current_object
    for art_type in ['painting', 'sculpture']:
        listbox = globals()[f"{art_type}s_list"]
        if listbox.curselection():
            item = listbox.get(listbox.curselection()[0])
            art_id = int(item.split('|')[0].split(':')[1].strip())
            
            if messagebox.askyesno("Confirm", f"Delete selected {art_type}?"):
                delete(art_type, art_id)
                add_to_history(f"Deleted {art_type} ID: {art_id}")
                refresh_lists()
                selected_obj_label.config(text="None")
                for widget in action_buttons_frame.winfo_children(): 
                    widget.destroy()
            return
    
    messagebox.showwarning("Warning", "Please select an item to delete")

def edit_selected():
    global current_edit_id
    for art_type in ['painting', 'sculpture']:
        listbox = globals()[f"{art_type}s_list"]
        if listbox.curselection():
            item = listbox.get(listbox.curselection()[0])
            current_edit_id = int(item.split('|')[0].split(':')[1].strip())
            show_edit_dialog(art_type, read(art_type, current_edit_id))
            return
    
    messagebox.showwarning("Warning", "Please select an item to edit")

def show_edit_dialog(art_type, data=None):
    dialog = tk.Toplevel()
    dialog.title(f"{'Edit' if data else 'Add'} {art_type.capitalize()}")
    
    fields = [
        ("Title", "text"),
        ("Author", "text"),
        ("Size" if art_type == 'painting' else "Weight", "number"),
        ("Color Type" if art_type == 'painting' else "Material", "text")
    ]
    
    entries = []
    for row, (label, _) in enumerate(fields):
        ttk.Label(dialog, text=f"{label}:").grid(row=row, column=0, padx=5, pady=5, sticky=tk.W)
        entry = ttk.Entry(dialog, width=30)
        entry.grid(row=row, column=1, padx=5, pady=5)
        if data and row < len(data)-1: 
            entry.insert(0, data[row+1])
        entries.append(entry)

    def save():
        global current_edit_id
        params = [e.get() for e in entries]
        try:
            params[2] = int(params[2]) if art_type == 'painting' else float(params[2])
            if data:
                update(art_type, [current_edit_id] + params)
                message = f"Updated {art_type}: {params[0]} by {params[1]}"
            else:
                create(art_type, params)
                message = f"Added new {art_type}: {params[0]} by {params[1]}"
            
            add_to_history(message)
            dialog.destroy()
            refresh_lists()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {str(e)}")
    
    ttk.Button(dialog, text="Save", command=save).grid(row=len(fields), column=0, columnspan=2, pady=10)

def add_to_history(message):
    action_history.append(message)
    update_history()

if __name__ == "__main__":
    root = tk.Tk()
    setup_ui(root)
    refresh_lists()
    root.mainloop()
