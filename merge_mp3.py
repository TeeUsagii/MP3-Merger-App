import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import time


class Mp3MergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MP3 Merger App")
        self.root.geometry("500x400")

        self.file_list = []

        # GUI Components
        self.label = tk.Label(root, text="Select MP3 files to merge:")
        self.label.pack(pady=10)

        self.listbox = tk.Listbox(root, width=60, height=15)
        self.listbox.pack(padx=10, pady=10)

        self.add_button = tk.Button(root, text="Add MP3 Files", command=self.add_files)
        self.add_button.pack(side=tk.LEFT, padx=10)

        self.remove_button = tk.Button(root, text="Remove Selected", command=self.remove_selected)
        self.remove_button.pack(side=tk.LEFT)

        self.remove_all_button = tk.Button(root, text="Remove All", command=self.remove_all)
        self.remove_all_button.pack(side=tk.LEFT, padx=5)

        self.merge_button = tk.Button(root, text="Merge Files", command=self.merge_files)
        self.merge_button.pack(side=tk.RIGHT, padx=10)

    def remove_all(self):
        self.file_list.clear()
        self.listbox.delete(0, tk.END)

    def add_files(self):
        files = filedialog.askopenfilenames(filetypes=[("MP3 files", "*.mp3")])
        for file in files:
            if file not in self.file_list:
                self.file_list.append(file)
                self.listbox.insert(tk.END, file)

    def remove_selected(self):
        selected_indices = self.listbox.curselection()
        for i in reversed(selected_indices):
            self.file_list.pop(i)
            self.listbox.delete(i)

    def merge_files(self):
        if len(self.file_list) < 2:
            messagebox.showerror("Error", "You need to select at least 2 files to merge.")
            return

        output_file = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
        if not output_file:
            return

        try:
            # Create input file list for ffmpeg
            with open("file_list.txt", "w", encoding="utf-8") as f:
                for file in self.file_list:
                    f.write(f"file '{file}'\n")

            # Run ffmpeg command using subprocess.run
            ffmpeg_path = os.path.join(os.path.dirname(__file__), "bin", "ffmpeg.exe")
            command = [ffmpeg_path, "-f", "concat", "-safe", "0", "-i", "file_list.txt", "-c", "copy",
                       "-ignore_unknown", "-err_detect", "ignore_err", output_file]
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            time.sleep(0.5)  # Đợi nửa giây để đảm bảo tiến trình ffmpeg giải phóng hoàn toàn

            messagebox.showinfo("Success", f"MP3 file has been successfully merged: {output_file}")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred while merging: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        finally:
            if os.path.exists("file_list.txt"):
                os.remove("file_list.txt")


if __name__ == "__main__":
    root = tk.Tk()
    app = Mp3MergerApp(root)
    root.mainloop()
