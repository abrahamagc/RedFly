import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
from pathlib import Path
import sys

class RedFlyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Red Fly Backup Tool")

        # Determine the base path for resources
        if hasattr(sys, '_MEIPASS'):
            self.base_path = sys._MEIPASS
        else:
            self.base_path = os.path.abspath(".")

        self.create_widgets()
        
    def create_widgets(self):
        # Load and display the logo
        logo_path = os.path.join(self.base_path, "redflylogo.png")
        self.logo = tk.PhotoImage(file=logo_path)
        self.logo_label = tk.Label(self.root, image=self.logo)
        self.logo_label.pack(pady=5)
        
        # Parent folder selection
        self.folder_label = tk.Label(self.root, text="Select Parent Folder:")
        self.folder_label.pack(pady=5)
        
        self.folder_entry = tk.Entry(self.root, width=50)
        self.folder_entry.pack(pady=5)
        
        self.browse_button = tk.Button(self.root, text="Browse", command=self.browse_folder)
        self.browse_button.pack(pady=5)
        
        # Prefix name entry
        self.prefix_label = tk.Label(self.root, text="Prefix Name:")
        self.prefix_label.pack(pady=5)
        
        self.prefix_entry = tk.Entry(self.root, width=50)
        self.prefix_entry.pack(pady=5)
        
        # Exclude folders entry with example button
        exclude_frame = tk.Frame(self.root)
        exclude_frame.pack(pady=5)
        
        self.exclude_label = tk.Label(exclude_frame, text="Exclude Folders (one per line):")
        self.exclude_label.pack(side=tk.LEFT)
        
        self.example_button = tk.Button(exclude_frame, text="Examples", command=self.show_examples)
        self.example_button.pack(side=tk.LEFT, padx=5)
        
        self.exclude_text = tk.Text(self.root, height=10, width=50)
        self.exclude_text.pack(pady=5)
        
        self.load_exclude_paths()
        
        # Log display for copied items
        self.log_copied_label = tk.Label(self.root, text="Log Copied:")
        self.log_copied_label.pack(pady=5)
        
        self.log_copied_text = tk.Text(self.root, height=10, width=50, state='disabled')
        self.log_copied_text.pack(pady=5)
        
        # Log display for excluded items
        self.log_excluded_label = tk.Label(self.root, text="Log Excluded:")
        self.log_excluded_label.pack(pady=5)
        
        self.log_excluded_text = tk.Text(self.root, height=10, width=50, state='disabled')
        self.log_excluded_text.pack(pady=5)
        
        # Backup button
        self.backup_button = tk.Button(self.root, text="Backup", command=self.backup_folder)
        self.backup_button.pack(pady=10)

        # Final folder name display
        self.final_folder_label = tk.Label(self.root, text="")
        self.final_folder_label.pack(pady=5)
    
    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder_selected)
    
    def load_exclude_paths(self):
        exclude_path = os.path.join(self.base_path, "exclude.txt")
        if os.path.exists(exclude_path):
            with open(exclude_path, "r") as file:
                exclude_paths = file.read()
                self.exclude_text.insert(tk.END, exclude_paths)
    
    def save_exclude_paths(self):
        exclude_path = os.path.join(self.base_path, "exclude.txt")
        with open(exclude_path, "w") as file:
            file.write(self.exclude_text.get("1.0", tk.END))
    
    def log_copied(self, message):
        self.log_copied_text.config(state='normal')
        self.log_copied_text.insert(tk.END, message + "\n")
        self.log_copied_text.config(state='disabled')
        self.log_copied_text.see(tk.END)
    
    def log_excluded(self, message, color='red'):
        self.log_excluded_text.config(state='normal')
        self.log_excluded_text.insert(tk.END, message + "\n", ('color',))
        self.log_excluded_text.tag_configure('color', foreground=color)
        self.log_excluded_text.config(state='disabled')
        self.log_excluded_text.see(tk.END)

    def show_examples(self):
        example_text = "Examples of exclude patterns:\ncheckpoints/\noutput/\nmodels/"
        messagebox.showinfo("Exclude Patterns Examples", example_text)
    
    def clear_logs(self):
        self.log_copied_text.config(state='normal')
        self.log_copied_text.delete("1.0", tk.END)
        self.log_copied_text.config(state='disabled')
        
        self.log_excluded_text.config(state='normal')
        self.log_excluded_text.delete("1.0", tk.END)
        self.log_excluded_text.config(state='disabled')
    
    def backup_folder(self):
        self.clear_logs()
        
        parent_folder = self.folder_entry.get()
        prefix_name = self.prefix_entry.get().strip()
        exclude_patterns = self.exclude_text.get("1.0", tk.END).strip().splitlines()
        
        if not parent_folder:
            messagebox.showerror("Error", "Please select a parent folder.")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_folder_name = f"{timestamp}_{prefix_name}_{os.path.basename(parent_folder)}" if prefix_name else f"{timestamp}_{os.path.basename(parent_folder)}"
        backup_folder_path = os.path.join(os.path.dirname(parent_folder), backup_folder_name)
        log_folder = './LOG'
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)
        log_file_path = os.path.join(log_folder, 'backup_log.txt')
        
        def should_exclude(path):
            relative_path = Path(path).relative_to(parent_folder)
            for pattern in exclude_patterns:
                if relative_path.match(pattern):
                    return True
            return False
        
        self.save_exclude_paths()
        
        try:
            with open(log_file_path, 'w') as log_file:
                for root, dirs, files in os.walk(parent_folder):
                    # Exclude specified folders
                    excluded_dirs = [d for d in dirs if should_exclude(os.path.join(root, d))]
                    dirs[:] = [d for d in dirs if not should_exclude(os.path.join(root, d))]
                    
                    # Log excluded folders
                    for dir in excluded_dirs:
                        log_message = f"Excluded folder: {os.path.join(root, dir)}"
                        log_file.write(f"\033[91m{log_message}\033[0m\n")
                        self.log_excluded(log_message, color='red')
                    
                    # Create corresponding directories in backup folder
                    for dir in dirs:
                        source_dir = os.path.join(root, dir)
                        target_dir = source_dir.replace(parent_folder, backup_folder_path, 1)
                        if not os.path.exists(target_dir):
                            os.makedirs(target_dir)
                    
                    # Copy files and log
                    for file in files:
                        source_file = os.path.join(root, file)
                        target_file = source_file.replace(parent_folder, backup_folder_path, 1)
                        if not should_exclude(source_file):
                            shutil.copy2(source_file, target_file)
                            log_message = f"Copied file: {source_file}"
                            log_file.write(f"{log_message}\n")
                            self.log_copied(log_message)
            
            messagebox.showinfo("Success", f"Backup completed successfully.\nBackup folder: {backup_folder_path}\nLog file: {log_file_path}")
            self.final_folder_label.config(text=f"Final Backup Folder: {backup_folder_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during backup: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RedFlyApp(root)
    root.mainloop()
