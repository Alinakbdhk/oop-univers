import tkinter as tk
from tkinter import messagebox


class CountHeap:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Решатель теории игр")
        self.root.geometry("850x550")

        self.choose_1or2 = None
        self.operations = []
        self.end_game_condition = None
        self.number_start_stone = None
        self.any_petya_move = False
        self.m1_count_stone = None

        self.create_interface()

    def create_interface(self):
        main_container = tk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        left_frame = tk.Frame(main_container)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        right_frame = tk.Frame(main_container, width=250)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(5, 0))

        self.create_solution_section(right_frame)
        self.create_settings_section(left_frame)

    def create_solution_section(self, parent):
        solution_frame = tk.Frame(parent, relief='solid', bd=1, bg='#f0f0f0')
        solution_frame.pack(fill=tk.BOTH, expand=True)

        solve_btn = tk.Button(solution_frame, text="Решить задания",
                              font=('Arial', 10), bg="lightgreen",
                              height=2, width=16,
                              command=self.solve_all_tasks)
        solve_btn.pack(pady=15)

        separator = tk.Frame(solution_frame, height=1, bg="gray")
        separator.pack(fill=tk.X, pady=5, padx=10)

        result_container = tk.Frame(solution_frame, bg='white', relief='solid', bd=1)
        result_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        self.solve_all_result_label = tk.Label(result_container, text="",
                                               font=('Arial', 9),
                                               wraplength=230,
                                               justify=tk.LEFT,
                                               bg='white',
                                               padx=8,
                                               pady=8)
        self.solve_all_result_label.pack(fill=tk.BOTH, expand=True)

    def create_settings_section(self, parent):
        mode_frame = tk.Frame(parent)
        mode_frame.pack(fill=tk.X, pady=(0, 8))

        tk.Label(mode_frame, text="Режим:", font=('Arial', 9)).pack(side=tk.LEFT)

        self.mode1_btn = tk.Button(mode_frame, text="1 кучка",
                                   font=('Arial', 8), width=8, height=1,
                                   command=lambda: self.select_mode(1))
        self.mode1_btn.pack(side=tk.LEFT, padx=3)

        self.mode2_btn = tk.Button(mode_frame, text="2 кучки",
                                   font=('Arial', 8), width=8, height=1,
                                   command=lambda: self.select_mode(2))
        self.mode2_btn.pack(side=tk.LEFT, padx=3)

        separator1 = tk.Frame(parent, height=1, bg="#e0e0e0")
        separator1.pack(fill=tk.X, pady=6)

        self.create_p_value_section(parent)

        separator2 = tk.Frame(parent, height=1, bg="#e0e0e0")
        separator2.pack(fill=tk.X, pady=6)

        self.create_initial_stones_section(parent)

        separator3 = tk.Frame(parent, height=1, bg="#e0e0e0")
        separator3.pack(fill=tk.X, pady=6)

        self.create_operations_section(parent)

        separator4 = tk.Frame(parent, height=1, bg="#e0e0e0")
        separator4.pack(fill=tk.X, pady=6)

        self.create_end_game_section(parent)

        separator5 = tk.Frame(parent, height=1, bg="#e0e0e0")
        separator5.pack(fill=tk.X, pady=6)

        self.create_task19_checkbox(parent)

    def create_p_value_section(self, parent):
        p_section = tk.Frame(parent)
        p_section.pack(fill=tk.X, pady=3)

        tk.Label(p_section, text="Камни в первой куче (p):",
                 font=('Arial', 9)).pack(anchor='w', pady=1)

        input_frame = tk.Frame(p_section)
        input_frame.pack(fill=tk.X, pady=3)

        tk.Label(input_frame, text="p =", font=('Arial', 8)).pack(side=tk.LEFT)

        self.p_entry = tk.Entry(input_frame, width=8,
                                font=('Arial', 8), justify='center')
        self.p_entry.pack(side=tk.LEFT, padx=3)

        save_p_btn = tk.Button(input_frame, text="Сохранить",
                               font=('Arial', 8), bg="lightblue",
                               command=self.save_p_value)
        save_p_btn.pack(side=tk.LEFT, padx=3)

        self.p_result_label = tk.Label(p_section, text="",
                                       font=('Arial', 8))
        self.p_result_label.pack(anchor='w', pady=1)

    def save_p_value(self):
        try:
            p_text = self.p_entry.get().strip()
            if not p_text:
                self.p_result_label.config(text="Ошибка: введите p!", fg="red")
                return

            p_value = int(p_text)
            if p_value < 0:
                self.p_result_label.config(text="Ошибка: p≥0!", fg="red")
                return

            self.m1_count_stone = p_value
            self.p_result_label.config(text=f"p = {p_value}", fg="green")

        except ValueError:
            self.p_result_label.config(text="Ошибка: число!", fg="red")

    def select_mode(self, mode):
        self.choose_1or2 = mode

        self.mode1_btn.config(bg="SystemButtonFace", relief="raised")
        self.mode2_btn.config(bg="SystemButtonFace", relief="raised")

        if mode == 1:
            self.mode1_btn.config(bg="lightblue", relief="sunken")
            for widget in self.root.winfo_children():
                if hasattr(widget, 'winfo_children'):
                    for child in widget.winfo_children():
                        if hasattr(child, 'winfo_children'):
                            for subchild in child.winfo_children():
                                if 'Камни в первой куче' in str(subchild):
                                    child.pack_forget()
        else:
            self.mode2_btn.config(bg="lightblue", relief="sunken")
            for widget in self.root.winfo_children():
                if hasattr(widget, 'winfo_children'):
                    for child in widget.winfo_children():
                        if hasattr(child, 'winfo_children'):
                            for subchild in child.winfo_children():
                                if 'Камни в первой куче' in str(subchild):
                                    child.pack(fill=tk.X, pady=3)

    def create_task19_checkbox(self, parent):
        checkbox_frame = tk.Frame(parent)
        checkbox_frame.pack(fill=tk.X, pady=3)

        self.task19_var = tk.BooleanVar()
        task19_checkbox = tk.Checkbutton(checkbox_frame,
                                         text="При любом ходе Пети (задание 19)",
                                         font=('Arial', 8),
                                         variable=self.task19_var,
                                         command=self.on_task19_checkbox_change)
        task19_checkbox.pack(anchor='w')

    def on_task19_checkbox_change(self):
        self.any_petya_move = self.task19_var.get()

    def create_end_game_section(self, parent):
        end_game_section = tk.Frame(parent)
        end_game_section.pack(fill=tk.X, pady=3)

        tk.Label(end_game_section, text="Конец игры:",
                 font=('Arial', 9)).pack(anchor='w', pady=1)

        tk.Label(end_game_section, text="Пример: '>= 50'",
                 font=('Arial', 7), fg='gray').pack(anchor='w', pady=1)

        input_frame = tk.Frame(end_game_section)
        input_frame.pack(fill=tk.X, pady=3)

        self.end_game_entry = tk.Entry(input_frame, width=35,
                                       font=('Arial', 8))
        self.end_game_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 3))
        self.end_game_entry.bind('<Return>',
                                 lambda event: self.save_end_game_condition())

        save_btn = tk.Button(input_frame, text="Сохранить",
                             font=('Arial', 8), bg="lightblue",
                             command=self.save_end_game_condition)
        save_btn.pack(side=tk.RIGHT)

    def save_end_game_condition(self):
        condition_text = self.end_game_entry.get().strip()

        if not condition_text:
            messagebox.showerror("Ошибка", "Введите условие!")
            return

        self.end_game_condition = condition_text

    def create_operations_section(self, parent):
        operations_section = tk.Frame(parent)
        operations_section.pack(fill=tk.X, pady=3)

        tk.Label(operations_section, text="Операции:",
                 font=('Arial', 9)).pack(anchor='w', pady=1)

        tk.Label(operations_section, text="Формат: для двух куч(m1+2 или m2//2), для одной кучи (m-4)",
                 font=('Arial', 7), fg='gray').pack(anchor='w', pady=1)

        input_frame = tk.Frame(operations_section)
        input_frame.pack(fill=tk.X, pady=3)

        self.operation_entry = tk.Entry(input_frame, width=25,
                                        font=('Arial', 8))
        self.operation_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 3))
        self.operation_entry.bind('<Return>',
                                  lambda event: self.save_operation())

        save_op_btn = tk.Button(input_frame, text="Добавить",
                                font=('Arial', 8), bg="lightblue",
                                command=self.save_operation)
        save_op_btn.pack(side=tk.RIGHT)

        self.operations_display_label = tk.Label(operations_section,
                                                 text="Нет операций",
                                                 font=('Arial', 8),
                                                 fg="gray",
                                                 wraplength=500,
                                                 justify=tk.LEFT,
                                                 anchor='w')
        self.operations_display_label.pack(fill=tk.X, pady=3)

        buttons_frame = tk.Frame(operations_section)
        buttons_frame.pack(fill=tk.X, pady=2)

        clear_btn = tk.Button(buttons_frame,
                              text="Очистить все",
                              font=('Arial', 8),
                              command=self.clear_operations)
        clear_btn.pack(side=tk.LEFT)

    def save_operation(self):
        operation_text = self.operation_entry.get().strip()

        if not operation_text:
            messagebox.showerror("Ошибка", "Введите операцию!")
            return

        if not self.validate_operation(operation_text):
            messagebox.showerror("Ошибка", "Некорректный формат!")
            return

        self.operations.append(operation_text)
        self.operation_entry.delete(0, tk.END)
        self.update_operations_display()

    def validate_operation(self, operation):
        operators = ['*', '+', '-', '//']
        return any(op in operation for op in operators)

    def update_operations_display(self):
        if self.operations:
            operations_text = "Операции: "
            for i, operation in enumerate(self.operations):
                operations_text += operation
                if i < len(self.operations) - 1:
                    operations_text += ", "

            self.operations_display_label.config(text=operations_text, fg="black")
        else:
            self.operations_display_label.config(text="Нет операций", fg="gray")

    def clear_operations(self):
        self.operations.clear()
        self.update_operations_display()

    def create_initial_stones_section(self, parent):
        stones_section = tk.Frame(parent)
        stones_section.pack(fill=tk.X, pady=3)

        tk.Label(stones_section, text="Начальные камни:",
                 font=('Arial', 9)).pack(anchor='w', pady=1)

        range_frame = tk.Frame(stones_section)
        range_frame.pack(fill=tk.X, pady=3)

        from_frame = tk.Frame(range_frame)
        from_frame.pack(side=tk.LEFT, padx=3)

        tk.Label(from_frame, text="От:", font=('Arial', 8)).pack()
        self.from_entry = tk.Entry(from_frame, width=8,
                                   font=('Arial', 8), justify='center')
        self.from_entry.pack(pady=1)

        to_frame = tk.Frame(range_frame)
        to_frame.pack(side=tk.LEFT, padx=3)

        tk.Label(to_frame, text="До:", font=('Arial', 8)).pack()
        self.to_entry = tk.Entry(to_frame, width=8,
                                 font=('Arial', 8), justify='center')
        self.to_entry.pack(pady=1)

        set_range_btn = tk.Button(range_frame, text="Установить",
                                  font=('Arial', 8), bg="lightblue",
                                  command=self.set_initial_stones_range)
        set_range_btn.pack(side=tk.LEFT, padx=5)

    def set_initial_stones_range(self):
        try:
            from_text = self.from_entry.get()
            to_text = self.to_entry.get()

            if not from_text and not to_text:
                self.number_start_stone = None
                return

            if from_text and not to_text:
                from_value = int(from_text)
                self.number_start_stone = f"от {from_value}"
                return

            if not from_text and to_text:
                to_value = int(to_text)
                self.number_start_stone = f"до {to_value}"
                return

            from_value = int(from_text)
            to_value = int(to_text)

            if from_value > to_value:
                messagebox.showerror("Ошибка", "'от' > 'до'!")
                return

            self.number_start_stone = f"от {from_value} до {to_value}"

        except ValueError:
            messagebox.showerror("Ошибка", "Некорректные числа!")

    def parse_end_game_condition(self, s1, s2=None):
        if not self.end_game_condition:
            return False

        condition = self.end_game_condition.lower()

        if s2 is None:
            s = s1
        else:
            s = s1 + s2

        if '>=' in condition:
            parts = condition.split('>=')
            if len(parts) == 2:
                try:
                    value = int(parts[1].strip())
                    return s >= value
                except:
                    pass
        elif '<=' in condition:
            parts = condition.split('<=')
            if len(parts) == 2:
                try:
                    value = int(parts[1].strip())
                    return s <= value
                except:
                    pass
        elif '>' in condition:
            parts = condition.split('>')
            if len(parts) == 2:
                try:
                    value = int(parts[1].strip())
                    return s > value
                except:
                    pass
        elif '<' in condition:
            parts = condition.split('<')
            if len(parts) == 2:
                try:
                    value = int(parts[1].strip())
                    return s < value
                except:
                    pass
        elif '==' in condition:
            parts = condition.split('==')
            if len(parts) == 2:
                try:
                    value = int(parts[1].strip())
                    return s == value
                except:
                    pass
        elif '=' in condition:
            parts = condition.split('=')
            if len(parts) == 2:
                try:
                    value = int(parts[1].strip())
                    return s == value
                except:
                    pass

        return False

    def apply_operation(self, s, operation):
        try:
            if '+' in operation:
                parts = operation.split('+')
                if len(parts) == 2:
                    value = int(parts[1].strip())
                    return s + value
            elif '-' in operation:
                parts = operation.split('-')
                if len(parts) == 2:
                    value = int(parts[1].strip())
                    return s - value
            elif '*' in operation:
                parts = operation.split('*')
                if len(parts) == 2:
                    value = int(parts[1].strip())
                    return s * value
            elif '//' in operation:
                parts = operation.split('//')
                if len(parts) == 2:
                    value = int(parts[1].strip())
                    if value != 0:
                        return s // value
        except:
            pass
        return s

    def f(self, s, k):
        """Функция для 1 кучки"""
        if self.parse_end_game_condition(s):
            return k % 2 == 0
        if k == 0:
            return 0

        h = []
        for operation in self.operations:
            new_s = self.apply_operation(s, operation)
            if new_s != s:
                h.append(self.f(new_s, k - 1))

        return any(h) if k % 2 != 0 else all(h)

    def f2(self, m1, m2, k):
        """Функция для 2 кучек"""
        if self.parse_end_game_condition(m1, m2):
            return k % 2 == 0
        if k == 0:
            return 0

        h = []

        for operation in self.operations:
            new_m1 = self.apply_operation(m1, operation)
            if new_m1 != m1:
                h.append(self.f2(new_m1, m2, k - 1))

        for operation in self.operations:
            new_m2 = self.apply_operation(m2, operation)
            if new_m2 != m2:
                h.append(self.f2(m1, new_m2, k - 1))

        return any(h) if k % 2 != 0 else all(h)

    def f19(self, s, k):
        """Функция для задания 19 (1 кучка)"""
        if self.parse_end_game_condition(s):
            return k % 2 == 0
        if k == 0:
            return 0

        h = []
        for operation in self.operations:
            new_s = self.apply_operation(s, operation)
            if new_s != s:
                h.append(self.f19(new_s, k - 1))

        if k % 2 != 0:
            return any(h)
        else:
            return all(h) if self.any_petya_move else any(h)

    def f19_2(self, m1, m2, k):
        """Функция для задания 19 (2 кучки)"""
        if self.parse_end_game_condition(m1, m2):
            return k % 2 == 0
        if k == 0:
            return 0

        h = []

        for operation in self.operations:
            new_m1 = self.apply_operation(m1, operation)
            if new_m1 != m1:
                h.append(self.f19_2(new_m1, m2, k - 1))

        for operation in self.operations:
            new_m2 = self.apply_operation(m2, operation)
            if new_m2 != m2:
                h.append(self.f19_2(m1, new_m2, k - 1))

        if k % 2 != 0:
            return any(h)
        else:
            return all(h) if self.any_petya_move else any(h)

    def format_answer(self, result):
        if isinstance(result, list):
            if not result:
                return "нет"
            else:
                sorted_result = sorted(result)
                return " ".join(map(str, sorted_result))
        else:
            return str(result)

    def solve_all_tasks(self):
        if not self.choose_1or2:
            self.solve_all_result_label.config(
                text="Ошибка: выберите режим!",
                fg="red"
            )
            return

        if not self.number_start_stone:
            self.solve_all_result_label.config(
                text="Ошибка: установите диапазон камней!",
                fg="red"
            )
            return

        if not self.end_game_condition:
            self.solve_all_result_label.config(
                text="Ошибка: установите условие конца!",
                fg="red"
            )
            return

        if not self.operations:
            self.solve_all_result_label.config(
                text="Ошибка: добавьте операции!",
                fg="red"
            )
            return

        y1 = 0
        y2 = 1000

        if self.number_start_stone:
            if 'от' in self.number_start_stone and 'до' in self.number_start_stone:
                parts = self.number_start_stone.split('до')
                if len(parts) == 2:
                    y1 = int(parts[0].replace('от', '').strip())
                    y2 = int(parts[1].strip()) + 1
            elif 'от' in self.number_start_stone:
                y1 = int(self.number_start_stone.replace('от', '').strip())
            elif 'до' in self.number_start_stone:
                y2 = int(self.number_start_stone.replace('до', '').strip()) + 1

        result_lines = []

        if self.choose_1or2 == 1:
            # Задание 19
            try:
                result19 = min(s for s in range(y1, y2) if self.f19(s, 2))
                formatted_19 = self.format_answer(result19)
                result_lines.append(f"19: {formatted_19}")
            except:
                result_lines.append("19: нет")

            # Задание 20
            try:
                result20 = [s for s in range(y1, y2) if not self.f(s, 1) and self.f(s, 3)]
                formatted_20 = self.format_answer(result20)
                result_lines.append(f"20: {formatted_20}")
            except:
                result_lines.append("20: нет")

            # Задание 21
            try:
                result21 = [s for s in range(y1, y2) if self.f(s, 2) < self.f(s, 4)]
                formatted_21 = self.format_answer(result21)
                result_lines.append(f"21: {formatted_21}")
            except:
                result_lines.append("21: нет")

        else:
            if not self.m1_count_stone:
                self.solve_all_result_label.config(
                    text="Ошибка: установите p!",
                    fg="red"
                )
                return

            # Задание 19
            try:
                result19 = min(s for s in range(y1, y2) if self.f19_2(self.m1_count_stone, s, 2))
                formatted_19 = self.format_answer(result19)
                result_lines.append(f"19: {formatted_19}")
            except:
                result_lines.append("19: нет")

            # Задание 20
            try:
                result20 = [s for s in range(y1, y2) if not self.f2(self.m1_count_stone, s, 1) and self.f2(self.m1_count_stone, s, 3)]
                formatted_20 = self.format_answer(result20)
                result_lines.append(f"20: {formatted_20}")
            except:
                result_lines.append("20: нет")

            # Задание 21
            try:
                result21 = [s for s in range(y1, y2) if self.f2(self.m1_count_stone, s, 2) < self.f2(self.m1_count_stone, s, 4)]
                formatted_21 = self.format_answer(result21)
                result_lines.append(f"21: {formatted_21}")
            except:
                result_lines.append("21: нет")

        result_text = "\n".join(result_lines)
        self.solve_all_result_label.config(text=result_text, fg="black", font=('Arial', 9))

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = CountHeap()
    app.run()