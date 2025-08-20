import os
import pandas as pd
import re
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

# Folder Legal Doc
EXPECTED_FOLDERS = ["FOTO TU", "KTP", "SHPTU", "SIPTU", "SPT"]

# Regex format file
CORRECT_PATTERN = re.compile(r"^(KTP|SHPTU|SIPTU|SPT|FOTO)-\s*([A-Z]\.[A-Za-z0-9]+\.[A-Za-z0-9]+\.\d+)\.(pdf|jpg|jpeg|png)$")

def pilih_folder():
    folder_path.set(filedialog.askdirectory())

def pilih_excel():
    excel_path.set(filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")]))

def cek_folder_dan_file():
    root_folder = folder_path.get()
    excel_file = excel_path.get()
    
    if not root_folder or not excel_file:
        messagebox.showerror("Error", "Pilih folder utama dan file Excel terlebih dahulu!")
        return
    
    try:
        df = pd.read_excel(excel_file)

        if "Nomor TU" not in df.columns:
            messagebox.showerror("Error", "Kolom 'Nomor TU' tidak ditemukan di Excel!")
            return

        valid_ids = set(df["Nomor TU"].astype(str))
        total_tu_excel = len(valid_ids)

        missing_folders = []
        summary = {}
        extra_files = {}
        wrong_format_files = {}

        for folder in EXPECTED_FOLDERS:
            folder_full_path = os.path.join(root_folder, folder)
            if not os.path.exists(folder_full_path):
                missing_folders.append(f"⚠️ Tidak ada folder {folder}")

        for folder in EXPECTED_FOLDERS:
            folder_full_path = os.path.join(root_folder, folder)
            if not os.path.exists(folder_full_path):
                continue

            total_files = 0
            valid_files = 0
            extra_files[folder] = []
            wrong_format_files[folder] = []

            for filename in os.listdir(folder_full_path):
                if filename.lower() == "desktop.ini":  
                    continue
                total_files += 1

                match = CORRECT_PATTERN.match(filename)
                if match:
                    nomor_tu = match.group(2)
                    if nomor_tu in valid_ids:
                        valid_files += 1
                    else:
                        extra_files[folder].append(filename)
                else:
                    wrong_format_files[folder].append(filename)

            summary[folder] = (valid_files, total_files)

        result_text.config(state="normal")
        result_text.delete(1.0, tk.END)

        if missing_folders:
            result_text.insert(tk.END, "Folder yang tidak ditemukan:\n")
            for msg in missing_folders:
                result_text.insert(tk.END, f"{msg}\n")
            result_text.insert(tk.END, "\n")

        result_text.insert(tk.END, f"Rekapitulasi File:\n")
        result_text.insert(tk.END, f"Total Nomor TU di {os.path.basename(root_folder)} yang terdaftar pada SITU: {total_tu_excel}\n\n")

        for folder, (valid, total) in summary.items():
            result_text.insert(tk.END, f"{folder}: {valid} / {total} ✅\n")

        if any(extra_files.values()):
            result_text.insert(tk.END, "\n🚨 File yang TIDAK sesuai:\n")
            for folder, files in extra_files.items():
                if files:
                    result_text.insert(tk.END, f"📂 {folder}:\n")
                    for file in files:
                        result_text.insert(tk.END, f"❌ {file}\n")
                    result_text.insert(tk.END, "\n")

        if any(wrong_format_files.values()):
            result_text.insert(tk.END, "\n⚠️ File dengan FORMAT SALAH:\n")
            for folder, files in wrong_format_files.items():
                if files:
                    result_text.insert(tk.END, f"📂 {folder}:\n")
                    for file in files:
                        result_text.insert(tk.END, f"⚠️ {file}\n")
                    result_text.insert(tk.END, "\n")

        if not missing_folders and all(valid == total for valid, total in summary.items()):
            result_text.insert(tk.END, "✅ Semua file sudah sesuai format dan terdaftar dalam Excel!\n")

        result_text.config(state="disabled")

    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

root = tk.Tk()
root.title("Cek Folder & Validasi Nama File")
root.geometry("700x500")

folder_path = tk.StringVar(root)
excel_path = tk.StringVar(root)

tk.Label(root, text="Pilih Folder Utama:").pack(pady=5)
tk.Entry(root, textvariable=folder_path, width=60).pack(pady=5)
tk.Button(root, text="Browse", command=pilih_folder).pack(pady=5)

tk.Label(root, text="Pilih File Excel (Daftar Nomor TU):").pack(pady=5)
tk.Entry(root, textvariable=excel_path, width=60).pack(pady=5)
tk.Button(root, text="Browse", command=pilih_excel).pack(pady=5)

tk.Button(root, text="Cek Folder & File", command=cek_folder_dan_file, fg="white", bg="blue").pack(pady=10)

result_text = scrolledtext.ScrolledText(root, height=20, width=90, state="disabled")
result_text.pack(pady=10)

root.mainloop()
