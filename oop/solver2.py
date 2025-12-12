import tkinter as tk
from tkinter import ttk
from itertools import product, permutations

formula = ''
f_lambda = None
list1 = list(product([0, 1], repeat=4))
data = [list(i) for i in list1]
rez = ['-'] * 16
entries = []
sp_true = []
table_frame = None
display_mode = None


def get_formula():
    global formula, f_lambda
    text = entry.get()
    formula = text.replace(" ", "").replace("∨", " or ").replace("∧", " and ").replace("≡", "==").replace("→",
                                                                                                          "<=").replace(
        "¬", " 1- ")
    try:
        f_lambda = eval(f"lambda x, y, z, w: {formula}")
    except Exception as e:
        print(f"Ошибка в формуле: {e}")
        return
    for i, el in enumerate(data):
        formula2 = f_lambda(el[0], el[1], el[2], el[3])
        rez[i] = str(int(formula2))
    create_table()
    print(sp_true)


def f(x, y, z, w):
    x_v = int(x)
    y_v = int(y)
    z_v = int(z)
    w_v = int(w)
    return str(int(f_lambda(x_v, y_v, z_v, w_v)))


def create_table2():
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)
    headers = ["?", "?", "?", "?", "F"]
    for col, header in enumerate(headers):
        label = ttk.Label(frame, text=header, borderwidth=1, relief="solid",
                          background="lightblue", width=15)
        label.grid(row=0, column=col, sticky="nsew")
    for row in range(1, 4):
        row_entries = []
        for col in range(5):
            entry1 = ttk.Entry(frame, text='', width=15, background="lightgreen", justify="center")
            entry1.grid(row=row, column=col, sticky="nsew")
            row_entries.append(entry1)
        entries.append(row_entries)


def get_data2():
    data2 = []
    for row_entry in entries:
        row_data = []
        for entry in row_entry:
            value = entry.get().strip()
            row_data.append(value)
        data2.append(row_data)
    return data2


def find_value():
    sp = get_data2()
    print(sp)
    empty_n = []
    for i, row in enumerate(sp):
        for j in range(4):
            if row[j] == "":
                empty_n.append((i, j))
    root.result_label = tk.Label(root, text="", font=("Arial", 12), fg="green")
    root.result_label.pack(pady=10, padx=10)
    for value in product([0, 1], repeat=len(empty_n)):
        sp_fil = [row[:] for row in sp]
        for ind, (i, j) in enumerate(empty_n):
            sp_fil[i][j] = str(value[ind])
        row_set = set(tuple(row[:4]) for row in sp_fil)
        if len(row_set) != 3:
            continue
        rez2 = [row[4] for row in sp_fil]
        for p in permutations('wxyz'):
            mat = True
            res = []
            for row in sp_fil:
                res.append(f(**dict(zip(p, row[:4]))))
                if f(**dict(zip(p, row[:4]))) != row[4]:
                    mat = False
                    break
            if mat and (res == rez2):
                root.result_label.config(text=f"Найдена перестановка: {''.join(p)}")
                return


def create_table():
    global table_frame

    if table_frame is not None:
        table_frame.destroy()

    table_frame = tk.Frame(root)
    table_frame.pack(padx=10, pady=10)

    headers = ["x", "y", "z", "w", "F"]
    for col, header in enumerate(headers):
        label = ttk.Label(table_frame, text=header, borderwidth=1, relief="solid",
                          background="lightblue", width=15)
        label.grid(row=0, column=col, sticky="nsew")

    filtered_data = []
    filtered_rez = []

    mode = display_mode.get()
    if mode == "all":
        filtered_data = data
        filtered_rez = rez
    elif mode == "true":
        for i, value in enumerate(rez):
            if value == '1':
                filtered_data.append(data[i])
                filtered_rez.append(rez[i])
    elif mode == "false":
        for i, value in enumerate(rez):
            if value == '0':
                filtered_data.append(data[i])
                filtered_rez.append(rez[i])

    sp_true.clear()
    for row, row_data in enumerate(filtered_data, 1):
        sp_row = []
        for col, value in enumerate(row_data):
            sp_row.append(str(value))
            label = ttk.Label(table_frame, text=value, borderwidth=1, relief="solid",
                              width=15, background="white", anchor="center")
            label.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
        sp_true.append(sp_row)

    for row, value in enumerate(filtered_rez, 1):
        sp_true[row - 1].append(value)
        label = ttk.Label(table_frame, text=value, borderwidth=1, relief="solid",
                          width=15, background="white", anchor="center")
        label.grid(row=row, column=4, sticky="nsew")


def update_table():
    if formula:
        create_table()


root = tk.Tk()
root.geometry("800x800")
root.title("ЕГЭ_2")

display_mode = tk.StringVar(value="all")

entry = tk.Entry(root)
entry.pack(padx=10, pady=10)

btn = tk.Button(root, text="Ввести", command=get_formula)
btn.pack(pady=5)

label_result = tk.Label(root, text="")
label_result.pack(pady=10)

mode_frame = tk.Frame(root)
mode_frame.pack(pady=10)

rb_all = tk.Radiobutton(mode_frame, text="Все значения (0 и 1)",
                        variable=display_mode, value="all", command=update_table)
rb_all.pack(side=tk.LEFT, padx=5)

rb_true = tk.Radiobutton(mode_frame, text="Только 1",
                         variable=display_mode, value="true", command=update_table)
rb_true.pack(side=tk.LEFT, padx=5)

rb_false = tk.Radiobutton(mode_frame, text="Только 0",
                          variable=display_mode, value="false", command=update_table)
rb_false.pack(side=tk.LEFT, padx=5)

create_table2()
btn_collect = tk.Button(root, text="Подобрать буквы", command=find_value)
btn_collect.pack(pady=5)

root.mainloop()

