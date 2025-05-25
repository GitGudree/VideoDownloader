import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import threading
import yt_dlp

# Store the selected download path (default = user's Downloads folder)
download_path = Path.home() / "Downloads"
default_profile_path = Path(r"C:\Users\askil\AppData\Roaming\librewolf\Profiles\xcpbryom.default-default")

def choose_folder(label):
    global download_path
    folder = filedialog.askdirectory()
    if folder:
        download_path = Path(folder)
        label.config(text=f"Download folder: {download_path}")

def download_video(profile_path, url, status_label, fix_audio):
    

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'outtmpl': str(download_path / '%(title)s.%(ext)s'),
        'cookiesfrombrowser': ('firefox', profile_path),
        'force_overwrite': True,
        'verbose': False,
        'noprogress': True,
        'noplaylist': True,
    }

    if fix_audio:
        ydl_opts['postprocessor_args'] = [
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-b:a', '192k',
            '-movflags', '+faststart'
        ]

    try:
        status_label.config(text="Downloading...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        status_label.config(text="Download complete!")
    except Exception as e:
        status_label.config(text=f"Error: {e}")
        messagebox.showerror("Download failed", str(e))

def start_download(profile_entry, url_entry, status_label, fix_audio_var):
    url = url_entry.get().strip()
    profile = profile_entry.get().strip()

    if not url:
        messagebox.showwarning("Missing URL", "Please enter a YouTube video URL.")
        return
    if not profile:
        profile = default_profile_path

    # Start download in background
    threading.Thread(
        target=download_video,
        args=(Path(profile), url, status_label, fix_audio_var.get()),
        daemon=True
    ).start()

# GUI setup
root = tk.Tk()
root.title("YouTube Downloader")



tk.Label(root, text="YouTube URL:").grid(row=0, column=0, padx=10, pady=10, sticky='w')
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10)



folder_label = tk.Label(root, text=f"Location: {download_path}")
folder_label.grid(row=1, column=1, sticky='w', padx=10)

folder_btn = tk.Button(root, text="Choose Folder", command=lambda: choose_folder(folder_label))
folder_btn.grid(row=1, column=0, sticky='e', padx=10)

download_btn = tk.Button(root, text="Download", command=lambda: start_download(profile_entry, url_entry, status_label, fix_audio_var))
download_btn.grid(row=1, column=1, sticky='e', padx=10, pady=10)

tk.Label(root, text="Profile path:").grid(row=2, column=0, padx=10, pady=10, sticky='w')
profile_entry = tk.Entry(root, width=50)
profile_entry.grid(row=2, column=1, padx=10, pady=10)

fix_audio_var = tk.BooleanVar(value=True)
fix_audio_checkbox = tk.Checkbutton(root, text="Fix audio (Opus → AAC)", variable=fix_audio_var)
fix_audio_checkbox.grid(row=3, column=1, sticky='w', padx=10)

status_label = tk.Label(root, text="Status: Idle")
status_label.grid(row=4, column=1, sticky='w', padx=10)

root.mainloop()