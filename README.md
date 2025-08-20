# 🗂️ Legal Document Validation App

## Overview
A Python desktop application built with **Tkinter** to validate scanned legal document files (SHPTU, SIPTU, KTP, SPT, Foto TU) for business units in a market.  
The app checks file completeness, filename correctness, and generates a summary report.

---

## Features
- 📂 Folder structure validation (`FOTO TU`, `KTP`, `SHPTU`, `SIPTU`, `SPT`)
- 🔍 Regex-based filename format checking  
- ✅ Cross-check file names against Excel list of registered unit numbers  
- ⚠️ Detects missing folders, typos, and wrong formats  
- 📊 Displays validation report in GUI  
- 💾 Export validation result to text file (planned feature)

---

## Tech Stack
- **Python 3**
- **Tkinter** (GUI)
- **Pandas** (Excel handling)
- **Regex** (filename validation)

---

## Usage
1. Select the **main folder** containing legal docs.
2. Select the **Excel file** containing the official unit list (`Nomor TU` column required).
3. Click **Cek Folder & File** to validate.
4. View the results directly in the app.

---

## Example Output
📊 Rekapitulasi File:
🔢 Total Nomor TU di Pasar A = 125

KTP: 120 / 125 ✅
SHPTU: 118 / 125 ✅
SIPTU: 119 / 125 ✅
SPT: 125 / 125 ✅
FOTO TU: 122 / 125 ✅

🚨 File yang TIDAK sesuai:
📂 SHPTU:
❌ SHPTU-XX001.pdf

⚠️ File dengan FORMAT SALAH:
📂 SIPTU:
⚠️ SIPTU-123.pdf

---

## Screenshots
<img width="696" height="531" alt="image" src="https://github.com/user-attachments/assets/5c35fdc4-954c-480a-a95c-1e9a1ca3e3d0" />

---

## Future Enhancements
1. Export results to Excel/PDF
2. Configurable expected folder structure
