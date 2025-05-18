import tkinter as tk
from tkinter import messagebox, ttk
from itertools import product

# Fungsi logika
def logika_or(a, b): return a or b
def logika_and(a, b): return a and b
def logika_not(a): return not a
def logika_xor(a, b): return a != b
def logika_implikasi(a, b): return not a or b
def logika_biimplikasi(a, b): return a == b

OPERATORS = {
    '∨': logika_or,
    '∧': logika_and,
    '⊕': logika_xor,
    '⇒': logika_implikasi,
    '⇔': logika_biimplikasi
}

PRIORITAS = {
    '¬': 3, '∧': 2, '∨': 2, '⊕': 1, '⇒': 1, '⇔': 1
}

def evaluate_expression(expr, values):
    output = []
    operators = []

    def apply_operator(op):
        if op == '¬':
            val = output.pop()
            output.append(logika_not(val))
        else:
            b = output.pop()
            a = output.pop()
            output.append(OPERATORS[op](a, b))

    for token in expr:
        if token in 'pqr':
            output.append(values.get(token, False))
        elif token == 'T':
            output.append(True)
        elif token == 'F':
            output.append(False)
        elif token == '¬':
            operators.append(token)
        elif token in OPERATORS:
            while (operators and operators[-1] in OPERATORS and
                   PRIORITAS[operators[-1]] >= PRIORITAS[token]):
                apply_operator(operators.pop())
            operators.append(token)
        elif token == '(':
            operators.append(token)
        elif token == ')':
            while operators and operators[-1] != '(':
                apply_operator(operators.pop())
            operators.pop()

    while operators:
        apply_operator(operators.pop())

    return output[0] if output else None

def validate_expression(expr):
    stack = []
    for char in expr:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack:
                return False, "Tanda kurung tutup ')' tidak memiliki pasangan."
            stack.pop()
    if stack:
        return False, "Tanda kurung buka '(' tidak memiliki pasangan."
    return True, ""

def mengevaluasi_hasil():
    expr = expression.get()
    is_valid, error_message = validate_expression(expr)
    if not is_valid:
        messagebox.showerror("Kesalahan", error_message)
        return
    try:
        if any(var in expr for var in 'pqr'):
            menampilkan_tabel_kebenaran()
        else:
            result = evaluate_expression(expr, {})
            result_text = "Hasil ekspresi: True" if result else "Hasil ekspresi: False"
            messagebox.showinfo("Hasil", result_text)
    except Exception as e:
        messagebox.showerror("Kesalahan", "Masukkan ekspresi logika yang valid.")

def membuat_tabel_kebenaran(expr):
    vars_used = sorted(set(char for char in expr if char in 'pqr'))
    possible_values = list(product([True, False], repeat=len(vars_used)))
    table = []

    for values in possible_values:
        truth_values = dict(zip(vars_used, values))
        result = evaluate_expression(expr, truth_values)
        row = [truth_values[var] for var in vars_used] + [result]
        table.append(row)

    return vars_used, table

def menampilkan_tabel_kebenaran():
    expr = expression.get()
    is_valid, error_message = validate_expression(expr)
    if not is_valid:
        messagebox.showerror("Kesalahan", error_message)
        return

    try:
        vars_used, table = membuat_tabel_kebenaran(expr)
        table_window = tk.Toplevel(root)
        table_window.title(f"Tabel Kebenaran")
        columns = vars_used + [expr]
        tree = ttk.Treeview(table_window, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col, anchor='center')
            tree.column(col, width=100, anchor='center')
        for row in table:
            tree.insert('', 'end', values=["True" if val else "False" for val in row])
        tree.pack(expand=True, fill='both', padx=10, pady=10)
    except Exception as e:
        messagebox.showerror("Kesalahan", "Masukkan ekspresi logika yang valid.")

def add_to_expression(char):
    expression.set(expression.get() + char)

def menghapus_ekspresi():
    expression.set("")

# GUI Tkinter
root = tk.Tk()
root.title("Kalkulator Logika")
root.configure(bg="#f0f4f8")  # Warna latar belakang

expression = tk.StringVar()

entry = tk.Entry(root, textvariable=expression, font=("Arial", 18), justify='center',
                 bg="#ffffff", fg="#333333")
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

buttons = [
    ('p', 1, 0), ('q', 1, 1), ('r', 1, 2), ('T', 1, 3),
    ('∨', 2, 0), ('¬', 2, 1), ('∧', 2, 2), ('Clear', 2, 3),
    ('⊕', 3, 0), ('⇒', 3, 1), ('⇔', 3, 2), ('Tabel', 3, 3),
    ('(', 4, 0), (')', 4, 1), ('F', 4, 2), ('Hasil', 4, 3)
]

for (text, row, col) in buttons:
    action = lambda t=text: add_to_expression(t) if t not in ['Clear', 'Tabel', 'Hasil'] else None
    if text == 'Clear':
        action = menghapus_ekspresi
    elif text == 'Tabel':
        action = menampilkan_tabel_kebenaran
    elif text == 'Hasil':
        action = mengevaluasi_hasil

    bg_color = "#d1e7dd" if text in ['Clear', 'Tabel', 'Hasil'] else "#e2e8f0"
    fg_color = "#000000"

    tk.Button(root, text=text, command=action, font=("Arial", 14),
              bg=bg_color, fg=fg_color, activebackground="#bcd0c7").grid(
        row=row, column=col, padx=5, pady=5, sticky="nsew")

root.mainloop()
