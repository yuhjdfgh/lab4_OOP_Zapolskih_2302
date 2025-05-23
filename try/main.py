from classes import *
from database_manager import *
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

class master:
    def __init__(self, root):
        self.root = root
        self.current_object = None
        self.current_edit_id = None
        self.action_history = []
        
        self.setup_ui()
        self.refresh_lists()
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.setup_lists_frame(main_frame)
        
        self.setup_info_frame(main_frame)
        
        self.setup_history_frame(main_frame)
    
    def setup_lists_frame(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Paintings:").pack(anchor=tk.W)
        self.paintings_list = tk.Listbox(frame, height=10, width=60)
        self.paintings_list.pack(fill=tk.X, padx=5, pady=5)
        self.paintings_list.bind('<<ListboxSelect>>', lambda e: self.on_art_select('painting'))

        ttk.Label(frame, text="Sculptures:").pack(anchor=tk.W)
        self.sculptures_list = tk.Listbox(frame, height=10, width=60)
        self.sculptures_list.pack(fill=tk.X, padx=5, pady=5)
        self.sculptures_list.bind('<<ListboxSelect>>', lambda e: self.on_art_select('sculpture'))
        
        buttons = [
            ("Delete", self.delete_selected),
            ("Update", self.edit_selected),
            ("Create Painting", lambda: self.show_edit_dialog('painting')),
            ("Create Sculpture", lambda: self.show_edit_dialog('sculpture')),
            ("Refresh Lists", self.refresh_lists)
        ]
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X)
        
        for text, cmd in buttons:
            ttk.Button(btn_frame, text=text, command=cmd).pack(side=tk.LEFT, padx=2)
    
    def setup_info_frame(self, parent):
        frame = ttk.Frame(parent, padding="10")
        frame.pack(side=tk.LEFT, fill=tk.Y)
        
        ttk.Label(frame, text="Selected Object:").pack(anchor=tk.W)
        self.selected_obj_label = ttk.Label(frame, text="None", wraplength=200)
        self.selected_obj_label.pack(anchor=tk.W, pady=5)
        
        ttk.Label(frame, text="Actions:").pack(anchor=tk.W, pady=(10, 0))
        self.action_buttons_frame = ttk.Frame(frame)
        self.action_buttons_frame.pack(fill=tk.X)
        self.clear_action_buttons()
    
    def setup_history_frame(self, parent):
        frame = ttk.Frame(parent, padding="10")
        frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Action History:").pack(anchor=tk.W)
        self.history_text = scrolledtext.ScrolledText(frame, width=40, height=20, wrap=tk.WORD)
        self.history_text.pack(fill=tk.BOTH, expand=True)
        self.history_text.config(state=tk.DISABLED)
        
        ttk.Button(frame, text="Clear History", command=self.clear_history).pack(pady=5)
    
    def clear_history(self):
        self.action_history = []
        self.update_history_display()
    
    def add_to_history(self, message):
        self.action_history.append(message)
        self.update_history_display()
    
    def update_history_display(self):
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        self.history_text.insert(tk.END, "\n".join(self.action_history))
        self.history_text.see(tk.END)
        self.history_text.config(state=tk.DISABLED)
    
    def clear_action_buttons(self):
        for widget in self.action_buttons_frame.winfo_children():
            widget.destroy()
    
    def update_action_buttons(self, art_object):
        self.clear_action_buttons()
        
        actions = {
            Painting: {
                "Watch": "watch",
                "Buy": "buy",
                "Transport": "transport",
                "Restore": "restore",
                "Varnish": "varnish",
                "Clean": "clean"
            },
            Sculpture: {
                "Watch": "watch",
                "Buy": "buy",
                "Transport": "transport",
                "Restore": "restore",
                "Fix": "fix",
                "Drop": "drop"
            }
        }.get(type(art_object), {})
        
        for name, action in actions.items():
            ttk.Button(
                self.action_buttons_frame,
                text=name,
                command=lambda a=action: self.execute_action(art_object, a)
            ).pack(fill=tk.X, pady=2)
    
    def execute_action(self, obj, action_name):
        result = getattr(obj, action_name)()
        self.add_to_history(f"{obj.get_title()}: {result}")
    
    def on_art_select(self, art_type):
        listbox = self.paintings_list if art_type == 'painting' else self.sculptures_list
        selection = listbox.curselection()
        
        if not selection:
            return
        
        item = listbox.get(selection[0])
        art_id = int(item.split('|')[0].split(':')[1].strip())
        
        data = read(art_type, art_id)
        
        #
        if art_type == 'painting':
            self.current_object = Painting(*data[1:])
            self.add_to_history(f"Selected painting: {data[1]} by {data[2]}")
        else:
            self.current_object = Sculpture(*data[1:])
            self.add_to_history(f"Selected sculpture: {data[1]} by {data[2]}")
        
        #
        self.selected_obj_label.config(
            text=f"{art_type.capitalize()}:\n{self.current_object.get_title()}\nby {self.current_object.get_author()}"
        )
        self.update_action_buttons(self.current_object)
    
    def refresh_lists(self):
        for listbox, art_type in [(self.paintings_list, 'painting'), 
                                 (self.sculptures_list, 'sculpture')]:
            listbox.delete(0, tk.END)
            items = get_all_paintings() if art_type == 'painting' else get_all_sculptures()
            
            for item in items:
                if art_type == 'painting':
                    listbox.insert(tk.END, 
                        f"ID: {item[0]} | {item[1]} by {item[2]} | Size: {item[3]} | Type: {item[4]}")
                else:
                    listbox.insert(tk.END, 
                        f"ID: {item[0]} | {item[1]} by {item[2]} | Weight: {item[3]} | Material: {item[4]}")
    
    def delete_selected(self):
        for listbox, art_type in [(self.paintings_list, 'painting'), 
                                 (self.sculptures_list, 'sculpture')]:
            selection = listbox.curselection()
            if selection:
                item = listbox.get(selection[0])
                art_id = int(item.split('|')[0].split(':')[1].strip())
                
                if messagebox.askyesno("Confirm", f"Delete selected {art_type}?"):
                    try:
                        delete(art_type, art_id)
                        self.add_to_history(f"Deleted {art_type} ID: {art_id}")
                        self.refresh_lists()
                        messagebox.showinfo("Success", f"{art_type.capitalize()} deleted")
                        self.current_object = None
                        self.selected_obj_label.config(text="None")
                        self.clear_action_buttons()
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to delete: {str(e)}")
                return
        
        messagebox.showwarning("Warning", "Please select an item to delete")
    
    def edit_selected(self):
        for listbox, art_type in [(self.paintings_list, 'painting'), 
                                 (self.sculptures_list, 'sculpture')]:
            selection = listbox.curselection()
            if selection:
                item = listbox.get(selection[0])
                self.current_edit_id = int(item.split('|')[0].split(':')[1].strip())
                data = read(art_type, self.current_edit_id)
                self.add_to_history(f"Editing {art_type} ID: {self.current_edit_id}")
                self.show_edit_dialog(art_type, data)
                return
        
        messagebox.showwarning("Warning", "Please select an item to edit")
    
    def show_edit_dialog(self, art_type, data=None):
        dialog = tk.Toplevel()
        dialog.title(f"{'Edit' if data else 'Add'} {art_type.capitalize()}")
        
        fields = [
            ("Title", "text"),
            ("Author", "text"),
            ("Size" if art_type == 'painting' else "Weight", "number"),
            ("Color Type" if art_type == 'painting' else "Material", "text")
        ]
        
        entries = []
        for row, (label, field_type) in enumerate(fields):
            ttk.Label(dialog, text=f"{label}:").grid(row=row, column=0, padx=5, pady=5, sticky=tk.W)
            entry = ttk.Entry(dialog, width=30)
            entry.grid(row=row, column=1, padx=5, pady=5)
            
            if data and row < len(data)-1:
                entry.insert(0, data[row+1])
            
            entries.append(entry)

        def save():
            try:
                params = [e.get() for e in entries]
                params[2] = int(params[2]) if art_type == 'painting' else float(params[2])
                
                if data:
                    update(art_type, [self.current_edit_id] + params)
                    message = f"Updated {art_type}: {params[0]} by {params[1]}"
                else:
                    create(art_type, params)
                    message = f"Added new {art_type}: {params[0]} by {params[1]}"
                
                self.add_to_history(message)
                dialog.destroy()
                self.refresh_lists()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric values")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save: {str(e)}")
        
        ttk.Button(dialog, text="Save", command=save).grid(row=len(fields), column=0, columnspan=2, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = master(root)
    root.mainloop()
