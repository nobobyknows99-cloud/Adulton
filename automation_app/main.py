import os
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

WINDOW_TITLE = "Automation App Starter"


def get_default_folder_map():
    return {
        "Images": {"jpg", "jpeg", "png", "gif", "bmp", "webp", "svg"},
        "Videos": {"mp4", "mov", "avi", "mkv", "wmv"},
        "Audio": {"mp3", "wav", "ogg", "flac"},
        "Documents": {"pdf", "doc", "docx", "txt", "rtf", "csv", "xlsx", "ppt", "pptx"},
        "Code": {"py", "js", "ts", "java", "cpp", "cs", "html", "css", "json", "xml", "sql"},
        "Archives": {"zip", "rar", "7z", "tar", "gz"},
        "Others": set(),
    }


def build_extension_map(folder_map):
    result = {}
    for folder_name, extensions in folder_map.items():
        for ext in extensions:
            result[ext.lower()] = folder_name
    return result


class AutomationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(WINDOW_TITLE)
        self.geometry("760x520")
        self.minsize(650, 420)

        self.source_path = tk.StringVar(value="")
        self.dest_path = tk.StringVar(value="")
        self.mode_var = tk.StringVar(value="move")

        self.folder_map = get_default_folder_map()
        self.extension_map = build_extension_map(self.folder_map)

        self.create_widgets()

    def create_widgets(self):
        pad_x = 12
        pad_y = 10

        main = ttk.Frame(self, padding=18)
        main.pack(fill="both", expand=True)

        ttk.Label(main, text="Source Folder:").grid(row=0, column=0, sticky="w", padx=pad_x, pady=pad_y)
        source_entry = ttk.Entry(main, textvariable=self.source_path, width=60)
        source_entry.grid(row=0, column=1, sticky="ew", padx=pad_x, pady=pad_y)
        ttk.Button(main, text="Browse", command=self.choose_source).grid(row=0, column=2, padx=pad_x, pady=pad_y)

        ttk.Label(main, text="Destination Folder:").grid(row=1, column=0, sticky="w", padx=pad_x, pady=pad_y)
        dest_entry = ttk.Entry(main, textvariable=self.dest_path, width=60)
        dest_entry.grid(row=1, column=1, sticky="ew", padx=pad_x, pady=pad_y)
        ttk.Button(main, text="Browse", command=self.choose_destination).grid(row=1, column=2, padx=pad_x, pady=pad_y)

        ttk.Label(main, text="Action:").grid(row=2, column=0, sticky="w", padx=pad_x, pady=pad_y)
        action_box = ttk.Combobox(
            main,
            textvariable=self.mode_var,
            values=[("Move files", "move"), ("Copy files", "copy")],
            state="readonly",
            width=18,
        )
        action_box.grid(row=2, column=1, sticky="w", padx=pad_x, pady=pad_y)

        ttk.Button(main, text="Run Automation", command=self.run_automation).grid(
            row=3, column=1, sticky="w", padx=pad_x, pady=(12, 10)
        )

        self.log_area = tk.Text(main, height=16, wrap="word", bg="#10141d", fg="#dfe6ff")
        self.log_area.grid(row=4, column=0, columnspan=3, sticky="nsew", padx=pad_x, pady=(0, 8))

        main.grid_columnconfigure(1, weight=1)
        main.grid_rowconfigure(4, weight=1)

    def log(self, message: str):
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.update_idletasks()

    def choose_source(self):
        folder = filedialog.askdirectory(title="Select source folder")
        if folder:
            self.source_path.set(folder)

    def choose_destination(self):
        folder = filedialog.askdirectory(title="Select destination folder")
        if folder:
            self.dest_path.set(folder)

    def run_automation(self):
        src = Path(self.source_path.get()).expanduser().resolve()
        dest = Path(self.dest_path.get()).expanduser().resolve()

        if not src.exists() or not src.is_dir():
            messagebox.showerror("Invalid source", "Please choose a valid source folder.")
            return

        if not dest.exists():
            try:
                dest.mkdir(parents=True, exist_ok=True)
            except OSError as exc:
                messagebox.showerror("Failed to create destination", str(exc))
                return

        mode = self.mode_var.get()
        self.log(f"Starting organizer in {mode} mode...")
        self.log(f"Source: {src}")
        self.log(f"Destination: {dest}")

        moved = 0
        skipped = 0
        errors = 0

        for item in src.iterdir():
            if item.is_dir():
                continue

            suffix = item.suffix.lower().lstrip('.')
            folder_name = self.extension_map.get(suffix, "Others")
            target_dir = dest / folder_name
            target_dir.mkdir(parents=True, exist_ok=True)

            target_path = target_dir / item.name

            try:
                if mode == "move":
                    if target_path == item:
                        continue
                    if target_path.exists():
                        unique_name = self.make_unique_name(target_path)
                        target_path = unique_name
                    shutil.move(str(item), str(target_path))
                else:
                    if target_path.exists():
                        unique_name = self.make_unique_name(target_path)
                        target_path = unique_name
                    shutil.copy2(str(item), str(target_path))

                moved += 1
                self.log(f"{item.name} -> {target_dir.name}")
            except Exception as exc:
                errors += 1
                self.log(f"ERROR: {item.name}: {exc}")

        self.log(f"Done. Moved/copied {moved} file(s), skipped {skipped}, errors {errors}.")
        messagebox.showinfo("Automation Complete", f"Processed {moved} files with {errors} errors.")

    @staticmethod
    def make_unique_name(path: Path) -> Path:
        stem = path.stem
        suffix = path.suffix
        counter = 1
        candidate = path
        while candidate.exists():
            candidate = path.with_name(f"{stem}_{counter}{suffix}")
            counter += 1
        return candidate


if __name__ == "__main__":
    app = AutomationApp()
    app.mainloop()
