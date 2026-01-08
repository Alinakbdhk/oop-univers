import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QLabel, QLineEdit, QComboBox
)
from PySide6.QtCore import Qt


class LogicSolverApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Решатель задач с отрезками')
        self.setGeometry(100, 100, 500, 350)

        # Основной layout
        main_layout = QVBoxLayout()

        # Заголовок
        title_label = QLabel("Найти длину отрезка A")
        title_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Выбор типа задачи
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Найти:"))
        self.task_type = QComboBox()
        self.task_type.addItems(["Наибольшую длину A", "Наименьшую длину A"])
        type_layout.addWidget(self.task_type)
        type_layout.addStretch()
        main_layout.addLayout(type_layout)

        # Поле для отрезка P
        p_layout = QHBoxLayout()
        p_layout.addWidget(QLabel("P = ["))
        self.p_start = QLineEdit()
        self.p_start.setFixedWidth(50)
        p_layout.addWidget(self.p_start)
        p_layout.addWidget(QLabel(";"))
        self.p_end = QLineEdit()
        self.p_end.setFixedWidth(50)
        p_layout.addWidget(self.p_end)
        p_layout.addWidget(QLabel("]"))
        p_layout.addStretch()
        main_layout.addLayout(p_layout)

        # Поле для отрезка Q
        q_layout = QHBoxLayout()
        q_layout.addWidget(QLabel("Q = ["))
        self.q_start = QLineEdit()
        self.q_start.setFixedWidth(50)
        q_layout.addWidget(self.q_start)
        q_layout.addWidget(QLabel(";"))
        self.q_end = QLineEdit()
        self.q_end.setFixedWidth(50)
        q_layout.addWidget(self.q_end)
        q_layout.addWidget(QLabel("]"))
        q_layout.addStretch()
        main_layout.addLayout(q_layout)

        # Поле для выражения
        expr_layout = QHBoxLayout()
        expr_layout.addWidget(QLabel("Выражение:"))
        self.expr = QLineEdit()
        self.expr.setText("¬(x ∈ A) → (((x ∈ P) ∧ (x ∈ Q)) → (x ∈ A))")
        main_layout.addLayout(expr_layout)
        main_layout.addWidget(self.expr)

        # Кнопки
        btn_layout = QHBoxLayout()
        self.solve_btn = QPushButton("Решить")
        self.solve_btn.clicked.connect(self.solve)
        btn_layout.addWidget(self.solve_btn)

        self.clear_btn = QPushButton("Очистить")
        self.clear_btn.clicked.connect(self.clear)
        btn_layout.addWidget(self.clear_btn)
        main_layout.addLayout(btn_layout)

        # Ответ
        self.answer = QTextEdit()
        self.answer.setReadOnly(True)
        self.answer.setMaximumHeight(80)
        main_layout.addWidget(QLabel("Ответ:"))
        main_layout.addWidget(self.answer)

        # Предустановленные значения для теста
        self.p_start.setText("17")
        self.p_end.setText("40")
        self.q_start.setText("20")
        self.q_end.setText("57")

        self.setLayout(main_layout)

    def solve(self):
        try:
            # Читаем данные
            p1 = int(self.p_start.text())
            p2 = int(self.p_end.text())
            q1 = int(self.q_start.text())
            q2 = int(self.q_end.text())
            expr = self.expr.text().strip()
            find_max = self.task_type.currentText() == "Наибольшую длину A"

            if p1 > p2 or q1 > q2:
                self.answer.setText("Ошибка: начало отрезка должна быть ≤ концу")
                return

            # Нормализуем выражение для анализа
            expr_norm = expr.replace(' ', '').replace('∈', 'in').lower()
            expr_norm = expr_norm.replace('≡', '=').replace('->', '→').replace('v', '∨').replace('∧', '&')
            expr_norm = expr_norm.replace('€', 'in').replace('e', 'in').replace('а', 'a').replace('д', '&')
            expr_norm = expr_norm.replace('¬', '!').replace('−', '!').replace('~', '!').replace('4', '→')
            expr_norm = expr_norm.replace('α', 'x').replace('a', 'x')  # для греческих букв

            # Определяем тип задачи
            if "((xinp)=(xinq))→!(xina)" in expr_norm or "≡" in expr:
                # Задача 1: ((x∈P)≡(x∈Q))→¬(x∈A)
                result = self.solve_task1(p1, p2, q1, q2, find_max)
            elif "!(xina)→(xinp)" in expr_norm and "→((xina)→(xinq))" in expr_norm:
                # Задача 2: (¬(x∈A)→(x∈P))→((x∈A)→(x∈Q))
                result = self.solve_task2(p1, p2, q1, q2, find_max)
            elif "((xina)→(xinp))∨(xinq)" in expr_norm:
                # Задача 3: ((x∈A)→(x∈P))∨(x∈Q)
                result = self.solve_task3(p1, p2, q1, q2, find_max)
            elif "(xinp)→(((xinq)&!(xina))→!(xinp))" in expr_norm:
                # Задача 4: (x∈P) → (((x∈Q) ∧ ¬(x∈A)) → ¬(x∈P))
                result = self.solve_task4(p1, p2, q1, q2, find_max)
            elif "!(xina)→((xinp)→!(xinq))" in expr_norm:
                # Задача 6: ¬(x∈A) → ((x∈P) → ¬(x∈Q))
                result = self.solve_task6(p1, p2, q1, q2, find_max)
            elif "!(xina)→((xinp)→(xinq))" in expr_norm:
                # Задача 5: ¬(x∈A) → ((x∈P) → (x∈Q))
                result = self.solve_task5(p1, p2, q1, q2, find_max)
            elif "!(xina)→(((xinp)&(xinq))→(xina))" in expr_norm:
                # Задача 7: ¬(x∈A) → (((x∈P) ∧ (x∈Q)) → (x∈A))
                result = self.solve_task7(p1, p2, q1, q2, find_max)
            else:
                # Пытаемся определить по структуре
                if "!(xina)→" in expr_norm and "((xinp)&(xinq))→(xina)" in expr_norm:
                    result = self.solve_task7(p1, p2, q1, q2, find_max)
                elif "!(xina)→" in expr_norm and "(xinp)→!(xinq)" in expr_norm:
                    result = self.solve_task6(p1, p2, q1, q2, find_max)
                elif "!(xina)→" in expr_norm and "(xinp)→(xinq)" in expr_norm:
                    result = self.solve_task5(p1, p2, q1, q2, find_max)
                elif "→!(xinp)" in expr_norm and expr_norm.count("→") >= 2:
                    result = self.solve_task4(p1, p2, q1, q2, find_max)
                elif "∨" in expr_norm or "v" in expr.lower():
                    result = self.solve_task3(p1, p2, q1, q2, find_max)
                elif "≡" in expr or "=" in expr_norm:
                    result = self.solve_task1(p1, p2, q1, q2, find_max)
                else:
                    result = "Неизвестный тип выражения"

            self.answer.setText(str(result))

        except ValueError:
            self.answer.setText("Ошибка: введите целые числа для границ отрезков")
        except Exception as e:
            self.answer.setText(f"Ошибка: {str(e)}")

    def solve_task1(self, p1, p2, q1, q2, find_max=True):
        """((x∈P)≡(x∈Q))→¬(x∈A)"""
        # Находим пересечение P и Q
        inter_start = max(p1, q1)
        inter_end = min(p2, q2)

        # Левая разрешенная область
        left_len = 0
        if min(p1, q1) < inter_start:
            left_len = inter_start - min(p1, q1)

        # Правая разрешенная область
        right_len = 0
        if inter_end < max(p2, q2):
            right_len = max(p2, q2) - inter_end

        return max(left_len, right_len) if find_max else 0

    def solve_task2(self, p1, p2, q1, q2, find_max=True):
        """(¬(x∈A)→(x∈P))→((x∈A)→(x∈Q))"""
        # A ⊆ Q, поэтому наибольшая длина A = длина Q
        # Наименьшая длина A = 0
        return (q2 - q1) if find_max else 0

    def solve_task3(self, p1, p2, q1, q2, find_max=True):
        """((x∈A)→(x∈P))∨(x∈Q)"""
        # Проверяем, пересекаются ли P и Q
        inter_start = max(p1, q1)
        inter_end = min(p2, q2)

        if find_max:
            if inter_start <= inter_end:
                # Пересекаются - можно взять объединение
                union_start = min(p1, q1)
                union_end = max(p2, q2)
                return union_end - union_start
            else:
                # Не пересекаются - берем больший из отрезков
                len_p = p2 - p1
                len_q = q2 - q1
                return max(len_p, len_q)
        else:
            # Наименьшая длина - можно взять пустое множество
            return 0

    def solve_task4(self, p1, p2, q1, q2, find_max=True):
        """(x∈P) → (((x∈Q) ∧ ¬(x∈A)) → ¬(x∈P))"""
        # Находим пересечение P и Q
        inter_start = max(p1, q1)
        inter_end = min(p2, q2)

        if inter_start > inter_end:
            # Нет пересечения
            if find_max:
                union_start = min(p1, q1)
                union_end = max(p2, q2)
                return union_end - union_start
            else:
                return 0
        else:
            # Есть пересечение
            intersection_length = inter_end - inter_start

            if find_max:
                union_start = min(p1, q1)
                union_end = max(p2, q2)
                return union_end - union_start
            else:
                return intersection_length

    def solve_task5(self, p1, p2, q1, q2, find_max=True):
        """¬(x∈A) → ((x∈P) → (x∈Q))"""
        # Упрощаем: (x∈A) ∨ ¬(x∈P) ∨ (x∈Q)
        # Ложно, когда: x∉A, x∈P, x∉Q
        # Значит A должно содержать точки из P, которые не в Q

        # Находим P \ Q
        # Это части P, которые не в Q

        inter_start = max(p1, q1)
        inter_end = min(p2, q2)

        if inter_start <= inter_end:
            # Есть пересечение
            left_len = 0
            if p1 < inter_start:
                left_len = inter_start - p1

            right_len = 0
            if inter_end < p2:
                right_len = p2 - inter_end

            if find_max:
                return max(left_len, right_len)
            else:
                # Наименьшая: берем минимальную ненулевую часть
                non_zero = [l for l in [left_len, right_len] if l > 0]
                return min(non_zero) if non_zero else 0
        else:
            # Нет пересечения
            len_p = p2 - p1
            return len_p

    def solve_task6(self, p1, p2, q1, q2, find_max=True):
        """¬(x∈A) → ((x∈P) → ¬(x∈Q))"""
        # Упрощаем: (x∈A) ∨ ¬(x∈P) ∨ ¬(x∈Q)
        # Ложно, когда: x∉A, x∈P, x∈Q
        # Значит A должно содержать все точки из P∩Q

        # Находим пересечение P и Q
        inter_start = max(p1, q1)
        inter_end = min(p2, q2)

        if inter_start <= inter_end:
            # Есть пересечение
            intersection_length = inter_end - inter_start

            if find_max:
                # Наибольшая длина: A может быть любым отрезком, содержащим пересечение
                union_start = min(p1, q1)
                union_end = max(p2, q2)
                return union_end - union_start
            else:
                # Наименьшая длина: нужно взять ровно пересечение
                return intersection_length
        else:
            # Нет пересечения
            if find_max:
                # Любой отрезок подойдет
                return 100
            else:
                # Подойдет даже пустое множество
                return 0

    def solve_task7(self, p1, p2, q1, q2, find_max=True):
        """¬(x∈A) → (((x∈P) ∧ (x∈Q)) → (x∈A))"""
        # Упрощаем:
        # ¬(x∈A) → (((x∈P) ∧ (x∈Q)) → (x∈A))
        # ≡ ¬(x∈A) → (¬((x∈P) ∧ (x∈Q)) ∨ (x∈A))
        # ≡ (x∈A) ∨ ¬((x∈P) ∧ (x∈Q)) ∨ (x∈A)
        # ≡ (x∈A) ∨ ¬(x∈P) ∨ ¬(x∈Q)

        # Выражение: (x∈A) ∨ ¬(x∈P) ∨ ¬(x∈Q)
        # Ложно, когда: (x∈A)=0 И ¬(x∈P)=0 И ¬(x∈Q)=0
        # То есть: x∉A И x∈P И x∈Q
        # То есть точки в пересечении P∩Q, которые не в A

        # Значит, чтобы выражение было истинно для всех x,
        # A должно содержать ВСЕ точки из P∩Q

        # Находим пересечение P и Q
        inter_start = max(p1, q1)
        inter_end = min(p2, q2)

        if inter_start <= inter_end:
            # Есть пересечение
            intersection_length = inter_end - inter_start

            if find_max:
                # Наибольшая длина: A может быть любым отрезком, содержащим пересечение
                # Можно взять весь P, весь Q, или их объединение
                union_start = min(p1, q1)
                union_end = max(p2, q2)
                return union_end - union_start
            else:
                # Наименьшая длина: нужно взять ровно пересечение
                return intersection_length
        else:
            # Нет пересечения
            if find_max:
                # Любой отрезок подойдет
                return 100
            else:
                # Подойдет даже пустое множество
                return 0

    def clear(self):
        self.p_start.clear()
        self.p_end.clear()
        self.q_start.clear()
        self.q_start.clear()
        self.expr.clear()
        self.answer.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LogicSolverApp()
    window.show()
    sys.exit(app.exec())