#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import re
import os
import html as html_lib

# --------------------- Parsing + writing HTML table --------------------- #

ROW_REGEX = re.compile(
    r'<tr>\s*'
    r'<td\s+bgcolor="(?P<color>[^"]+)">(?P<kw>[^<]+)</td>\s*'
    r'<td>(?P<text>.*?)</td>\s*'
    r'</tr>',
    re.DOTALL | re.IGNORECASE
)

DEFAULT_HEADER = """<!--------------------------- To-Do List by Hamza Ali Imran --------------------------->
<tr>
    <td>&nbsp;</td>
    <td>&nbsp;</td>
</tr>
<tr>        
    <th bgcolor="lightgrey">Hamza Ali Imran</th>
    <td bgcolor="lightgrey">&nbsp;</td>
</tr>
<!------------------------------------------------------------------------------------->
<tr>
    <td>&nbsp;</td>
    <td>&nbsp;</td>
</tr>

"""

DEFAULT_FOOTER = """
<tr>
    <td colspan="2">Long-Term To-Do</td>
</tr>

<tr>
    <td>&nbsp;</td>
    <td>&nbsp;</td>
</tr>
<!--------------------------- End of To-Do List by Hamza Ali Imran ---------------------->
"""

def parse_todo_file(text):
    """
    Parse the HTML-like to-do file.
    Returns: header, entries(list), footer
    entries = [{'kw': 'KW47', 'color': 'yellow', 'text': '...'}, ...]
    """
    matches = list(ROW_REGEX.finditer(text))
    if not matches:
        # No KW rows found → treat whole file as header, no entries, empty footer
        return text, [], ""

    header_start = 0
    header_end = matches[0].start()
    footer_start = matches[-1].end()
    footer_end = len(text)

    header = text[header_start:header_end]
    footer = text[footer_start:footer_end]

    entries = []
    for m in matches:
        color = m.group("color").strip()
        kw = m.group("kw").strip()
        raw_text = m.group("text").strip()
        # Unescape HTML entities for editing
        clean_text = html_lib.unescape(raw_text)
        entries.append({"kw": kw, "color": color, "text": clean_text})

    return header, entries, footer


def build_todo_text(header, entries, footer):
    """
    Build full HTML text from header, entries and footer.
    """
    body_parts = []
    for e in entries:
        kw = e["kw"]
        color = e["color"]
        text = e["text"]
        # Escape HTML special chars
        safe_text = html_lib.escape(text)
        row = (
            '<tr>   \n'
            f'    <td bgcolor="{color}">{kw}</td>\n'
            f'    <td>{safe_text}</td>\n'
            '</tr>\n\n'
        )
        body_parts.append(row)

    body = "".join(body_parts)
    return header + body + footer


def sort_entries_by_kw(entries):
    """
    Sort entries by numeric part of KW (e.g. KW43, KW47).
    """
    def kw_key(e):
        kw = e["kw"].strip().upper()
        m = re.search(r'(\d+)', kw)
        if m:
            return int(m.group(1))
        return 9999
    return sorted(entries, key=kw_key)


# --------------------- GUI Application --------------------- #

class TodoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("KW To-Do List Editor")

        self.current_file = None
        self.header = DEFAULT_HEADER
        self.footer = DEFAULT_FOOTER
        self.entries = []

        self._build_menu()
        self._build_main_layout()
        self._refresh_list()

    def _build_menu(self):
        menubar = tk.Menu(self.root)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.new_file)
        filemenu.add_command(label="Open...", command=self.open_file)
        filemenu.add_command(label="Save", command=self.save_file)
        filemenu.add_command(label="Save As...", command=self.save_file_as)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        self.root.config(menu=menubar)

    def _build_main_layout(self):
        # Top: file label + sort button
        top_frame = ttk.Frame(self.root, padding=5)
        top_frame.pack(fill="x")

        self.file_label_var = tk.StringVar(value="No file loaded")
        file_label = ttk.Label(top_frame, textvariable=self.file_label_var)
        file_label.pack(side="left", expand=True, fill="x")

        sort_button = ttk.Button(top_frame, text="Sort by KW", command=self.sort_by_kw)
        sort_button.pack(side="right")

        # Middle: list of items
        middle_frame = ttk.Frame(self.root, padding=5)
        middle_frame.pack(fill="both", expand=True)

        columns = ("kw", "color", "text")
        self.tree = ttk.Treeview(middle_frame, columns=columns, show="headings", height=12)
        self.tree.heading("kw", text="KW")
        self.tree.heading("color", text="Color")
        self.tree.heading("text", text="Description")

        self.tree.column("kw", width=60, anchor="center")
        self.tree.column("color", width=80, anchor="center")
        self.tree.column("text", width=500, anchor="w")

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        vsb = ttk.Scrollbar(middle_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # Bottom: editor
        bottom_frame = ttk.LabelFrame(self.root, text="Edit entry", padding=5)
        bottom_frame.pack(fill="x", padx=5, pady=5)

        # KW + Color
        row1 = ttk.Frame(bottom_frame)
        row1.pack(fill="x", pady=2)

        ttk.Label(row1, text="KW:").pack(side="left")
        self.kw_var = tk.StringVar(value="KW48")
        kw_entry = ttk.Entry(row1, textvariable=self.kw_var, width=10)
        kw_entry.pack(side="left", padx=(5, 15))

        ttk.Label(row1, text="Color:").pack(side="left")
        self.color_var = tk.StringVar(value="lightblue")
        color_options = ["yellow", "lightgreen", "lightblue", "magenta"]
        color_menu = ttk.OptionMenu(row1, self.color_var, self.color_var.get(), *color_options)
        color_menu.pack(side="left")

        # Description
        row2 = ttk.Frame(bottom_frame)
        row2.pack(fill="both", pady=2)

        ttk.Label(row2, text="Description:").pack(anchor="w")
        self.text_widget = tk.Text(row2, height=4, wrap="word")
        self.text_widget.pack(fill="x", expand=True)

        # Buttons
        row3 = ttk.Frame(bottom_frame)
        row3.pack(fill="x", pady=5)

        add_button = ttk.Button(row3, text="Add / Update", command=self.add_or_update_entry)
        add_button.pack(side="left", padx=5)

        delete_button = ttk.Button(row3, text="Delete", command=self.delete_entry)
        delete_button.pack(side="left", padx=5)

        clear_button = ttk.Button(row3, text="Clear form", command=self.clear_form)
        clear_button.pack(side="left", padx=5)

    # ---------- File operations ---------- #

    def new_file(self):
        if not self._confirm_discard_changes():
            return
        self.current_file = None
        self.header = DEFAULT_HEADER
        self.footer = DEFAULT_FOOTER
        self.entries = []
        self.file_label_var.set("New file (unsaved)")
        self._refresh_list()
        self.clear_form()

    def open_file(self):
        if not self._confirm_discard_changes():
            return
        filename = filedialog.askopenfilename(
            title="Open To-Do File",
            filetypes=[
                ("HTML or text files", "*.html *.htm *.txt"),
                ("All files", "*.*"),
            ],
        )
        if not filename:
            return
        try:
            with open(filename, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file:\n{e}")
            return

        header, entries, footer = parse_todo_file(text)
        self.current_file = filename
        self.header = header
        self.entries = entries
        self.footer = footer
        self.file_label_var.set(os.path.basename(filename))
        self._refresh_list()
        self.clear_form()

    def save_file(self):
        if self.current_file is None:
            self.save_file_as()
            return
        try:
            text = build_todo_text(self.header, self.entries, self.footer)
            with open(self.current_file, "w", encoding="utf-8") as f:
                f.write(text)
            messagebox.showinfo("Saved", f"Saved to: {self.current_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{e}")

    def save_file_as(self):
        filename = filedialog.asksaveasfilename(
            title="Save To-Do File As",
            defaultextension=".html",
            filetypes=[
                ("HTML files", "*.html *.htm"),
                ("Text files", "*.txt"),
                ("All files", "*.*"),
            ],
        )
        if not filename:
            return
        self.current_file = filename
        self.file_label_var.set(os.path.basename(filename))
        self.save_file()

    def _confirm_discard_changes(self):
        # Simple version: always ask; you could add tracking of "dirty" state
        if self.entries:
            ans = messagebox.askyesno(
                "Discard changes?",
                "Opening/creating a file will discard current list if not saved.\nContinue?"
            )
            return ans
        return True

    # ---------- List / selection handling ---------- #

    def _refresh_list(self):
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Insert entries
        for idx, e in enumerate(self.entries):
            short_text = e["text"].replace("\n", " ")
            if len(short_text) > 80:
                short_text = short_text[:77] + "..."
            self.tree.insert("", "end", iid=str(idx),
                             values=(e["kw"], e["color"], short_text))

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        idx = int(selected[0])
        e = self.entries[idx]
        self.kw_var.set(e["kw"])
        self.color_var.set(e["color"])
        self.text_widget.delete("1.0", "end")
        self.text_widget.insert("1.0", e["text"])

    # ---------- Entry operations ---------- #

    def add_or_update_entry(self):
        kw = self.kw_var.get().strip()
        color = self.color_var.get().strip()
        text = self.text_widget.get("1.0", "end").strip()

        if not kw:
            messagebox.showerror("Error", "KW cannot be empty (e.g. KW48).")
            return
        if not kw.upper().startswith("KW"):
            kw = "KW" + kw  # small convenience

        entry = {"kw": kw, "color": color, "text": text}

        selected = self.tree.selection()
        if selected:
            # Update existing
            idx = int(selected[0])
            self.entries[idx] = entry
        else:
            # Add new
            self.entries.append(entry)

        self._refresh_list()
        self.clear_form()

    def delete_entry(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Delete", "No entry selected.")
            return
        idx = int(selected[0])
        del self.entries[idx]
        self._refresh_list()
        self.clear_form()

    def clear_form(self):
        self.kw_var.set("KW48")
        self.color_var.set("lightblue")
        self.text_widget.delete("1.0", "end")
        self.tree.selection_remove(*self.tree.selection())

    def sort_by_kw(self):
        self.entries = sort_entries_by_kw(self.entries)
        self._refresh_list()


def main():
    root = tk.Tk()
    app = TodoGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
