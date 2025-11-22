
# 📘 KW To-Do List Editor

### A Python-Based GUI Tool for Managing Weekly KW To-Do Tables

This repository contains a lightweight, cross-platform Python GUI application that helps you **create, edit, and maintain weekly KW (Kalenderwoche) to-do lists**.
It is designed specifically for workflows where tasks are recorded in HTML table format, such as the file you uploaded:
`/mnt/data/HamzaAli_Imran_2025_KW48.txt`.

The tool lets you open existing KW task tables, edit entries, add new ones, sort by week number, and save them back in the same format—preserving headers, footers, colors, and layout.

---

## ✨ Features

* **Open existing KW HTML/txt to-do files**
* **Parse tasks automatically**
  Detects rows like:

  ```html
  <tr>
      <td bgcolor="yellow">KW47</td>
      <td>Continue normalization and drift mitigation…</td>
  </tr>
  ```
* **Add / edit / delete entries** via GUI
* **Preserve original header and footer**
* **Sort tasks by KW numeric value**
* **Color presets** (yellow, magenta, lightgreen, lightblue)
* **HTML-safe escaping** for special characters
* **Create new KW files from a template**
* **100% no external dependencies** — runs on stock Python + Tkinter
* **Works on Linux, macOS, and Windows**

---

## 🖼️ Screenshot (Placeholder)

> (Insert screenshot once you run the app and take an image.)

```
+-----------------------------------------------------------+
| File: KW48 Tasks                                          |
| [Sort by KW]                                              |
+-----------------------------------------------------------+
| KW   | Color       | Description                          |
| KW47 | lightgreen  | Prepare update slides…               |
| KW48 | lightblue   | Rewrite results section…             |
| ...                                                     … |
+-----------------------------------------------------------+
| Edit Entry                                                |
| KW: [KW48]     Color: [lightblue ▼]                      |
| Description:                                             |
| -------------------------------------------------------- |
| | Rewrite results section as per Akshay’s instructions | |
| -------------------------------------------------------- |
| [Add/Update] [Delete] [Clear Form]                       |
+-----------------------------------------------------------+
```

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/kw-todo-gui.git
cd kw-todo-gui
```

### 2. Install Tkinter (Linux only, if missing)

**Debian/Ubuntu:**

```bash
sudo apt-get install python3-tk
```

**Fedora:**

```bash
sudo dnf install python3-tkinter
```

Tkinter is already included on:

* macOS Python installer
* Windows Python installer

### 3. (Optional) Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## ▶️ Running the Application

```bash
python3 kw_todo_gui.py
```

The GUI window will open.

---

## 📁 File Format Support

The tool works with files containing HTML table rows such as:

```html
<tr>   
    <td bgcolor="yellow">KW47</td>
    <td>Continue working on normalization and drift mitigation methods.</td>
</tr>
```

The app will:

* Parse all rows
* Extract KW, color, and description
* Preserve **header** and **footer** sections exactly as-is

Your example file (uploaded):

```
/mnt/data/HamzaAli_Imran_2025_KW48.txt
```

is 100% supported.

---

## 🛠️ Usage Guide

### ✔️ Opening a File

1. Go to **File → Open**
2. Select a `.html` or `.txt` file
3. All KW rows will appear in a table view

---

### ✔️ Adding a New Task

1. Enter:

   * **KW** (e.g., `KW48`)
   * **Color**
   * **Task description**
2. Click **Add / Update**

---

### ✔️ Editing an Existing Task

1. Click on the entry in the list
2. Fields auto-populate
3. Modify and click **Add / Update**

---

### ✔️ Sorting Tasks

Click **“Sort by KW”** — sorting uses the **numeric** part of KW:

* KW43
* KW46
* KW47
* KW48
* …

---

### ✔️ Deleting a Task

1. Select a row
2. Click **Delete**

---

### ✔️ Creating a New File

Use **File → New**, then save via:

**File → Save As**

A default header/footer is auto-created.

---

## 🏗️ Project Structure (Recommended)

```
kw-todo-gui/
│
├── kw_todo_gui.py      # Main application
├── README.md           # This documentation
└── examples/
    └── sample_tasklist.html   # Optional example
```

---

## 🧠 Architecture Overview

### ✓ `parse_todo_file(text)`

Extracts rows into a list of dictionaries:

```python
{
  "kw": "KW47",
  "color": "lightgreen",
  "text": "Prepare update slides..."
}
```

### ✓ `build_todo_text(header, entries, footer)`

Reconstructs a full HTML file.

### ✓ GUI Components

* **TreeView** (shows KW + color + short text)
* **Editable form** (for KW, color, description)
* **File menu** (New, Open, Save, Save As)
* **Sort button**

No external dependencies.
Everything is written with `tkinter`, `html`, and `re`.

---

## 🔄 Suggested Weekly Workflow

```bash
cp KW48.html KW49.html     # duplicate last week’s file
python3 kw_todo_gui.py     # update tasks using GUI
git add KW49.html
git commit -m "Add KW49 tasks"
```

---

## 📤 Deployment (GitHub)

Just push your repo:

```bash
git add .
git commit -m "Add KW To-Do List GUI tool"
git push
```

Anyone can run it with:

```bash
python3 kw_todo_gui.py
```

---

## 🤝 Contributing

Pull requests are welcome!

Suggested improvements:

* Dark mode UI
* Export to Markdown / PDF
* Priority/Status column
* CSV import/export
* Color legend on GUI

---


## 📬 Support

If you want:

* More automation (e.g., auto-generate next KW file)
* A dashboard with charts
* A web version (Flask/Streamlit)

I can generate those extensions as well.

