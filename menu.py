import sys
from utils import clear_screen, get_key, hide_cursor, show_cursor, get_terminal_size
from config import COLORS

class InteractiveMenu:
    def __init__(self):
        self.options = [
            {"name": "Waterfall (Водопад)", "type": "mode", "value": "waterfall"},
            {"name": "Decoder (Дешифратор)", "type": "mode", "value": "decoder"},
            {"name": "Matrix Rain (Матрица)", "type": "mode", "value": "matrix"},
            {"name": "Slide (Слайдер)", "type": "mode", "value": "slide"},
        ]
        self.colors = [
            {"name": "Зеленый Неон", "value": "GREEN"},
            {"name": "Кибер-Голубой", "value": "CYAN"},
            {"name": "Кислотно-Красный", "value": "RED"},
            {"name": "Желтый Электрик", "value": "YELLOW"},
            {"name": "Фиолетовый", "value": "MAGENTA"},
            {"name": "Радужный Градиент", "theme": "rainbow"},
            {"name": "Огненный Градиент", "theme": "fire"},
            {"name": "Ледяной Градиент", "theme": "ice"}
        ]
        self.selected_mode_idx = 0
        self.selected_color_idx = 0
        self.step = 0 # 0: выбор режима, 1: выбор цвета, 2: ввод слова

    def draw_banner(self):
        cols, _ = get_terminal_size()
        banner = [
            r"  ___ _       _               ___                     _ ",
            r" / __(_)_ __ | |_  ___ _ _   / __|__ _ ___ __ __ _ __| |___ ",
            r"| (__| | '_ \| ' \/ -_) '_| | (__/ _` (_-</ _/ _` / _` / -_)",
            r" \___|_| .__/|_||_\___|_|    \___\__,_/__/\__\__,_\__,_\___|",
            r"       |_|                                                  ",
            r"============================================================"
        ]
        for line in banner:
            padding = " " * ((cols - len(line)) // 2)
            print(f"{COLORS['CYAN']}{padding}{line}{COLORS['RESET']}")
        print("\n")

    def run(self):
        hide_cursor()
        word = ""
        mode = ""
        color = "GREEN"
        theme = None

        while True:
            clear_screen()
            self.draw_banner()
            cols, _ = get_terminal_size()

            if self.step == 0:
                title = "=== ВЫБЕРИ РЕЖИМ АНИМАЦИИ ==="
                print(" " * ((cols - len(title)) // 2) + f"{COLORS['BOLD']}{title}{COLORS['RESET']}\n")
                for i, opt in enumerate(self.options):
                    pointer = "➔ " if i == self.selected_mode_idx else "  "
                    color_pre = COLORS["CYAN"] if i == self.selected_mode_idx else COLORS["WHITE"]
                    line = f"{pointer} {opt['name']}"
                    print(" " * ((cols - len(line)) // 2) + f"{color_pre}{line}{COLORS['RESET']}")
                
                print("\n" + " " * ((cols - 30) // 2) + f"{COLORS['RESET']}[Вверх/Вниз] - Выбор, [Enter] - Далее")

            elif self.step == 1:
                title = "=== ВЫБЕРИ СТИЛЬ ЦВЕТА ==="
                print(" " * ((cols - len(title)) // 2) + f"{COLORS['BOLD']}{title}{COLORS['RESET']}\n")
                for i, col_opt in enumerate(self.colors):
                    pointer = "➔ " if i == self.selected_color_idx else "  "
                    color_pre = COLORS["YELLOW"] if i == self.selected_color_idx else COLORS["WHITE"]
                    line = f"{pointer} {col_opt['name']}"
                    print(" " * ((cols - len(line)) // 2) + f"{color_pre}{line}{COLORS['RESET']}")
                
                print("\n" + " " * ((cols - 30) // 2) + f"{COLORS['RESET']}[Вверх/Вниз] - Выбор, [Enter] - Далее")

            elif self.step == 2:
                show_cursor()
                title = "=== ВВЕДИ СВОЁ СЛОВО ==="
                print(" " * ((cols - len(title)) // 2) + f"{COLORS['BOLD']}{title}{COLORS['RESET']}\n")
                prompt = "Слово: "
                sys.stdout.write(" " * ((cols - 20) // 2) + prompt)
                sys.stdout.flush()
                word = input()
                if word.strip() == "":
                    word = "ХАКЕР_ПИТОН"
                break

            # Обработка нажатия клавиш
            key = get_key()
            if key in ("arrow_[A", "arrow_up", "arrow_OA"):  # Вверх
                if self.step == 0:
                    self.selected_mode_idx = (self.selected_mode_idx - 1) % len(self.options)
                elif self.step == 1:
                    self.selected_color_idx = (self.selected_color_idx - 1) % len(self.colors)
            elif key in ("arrow_[B", "arrow_down", "arrow_OB"):  # Вниз
                if self.step == 0:
                    self.selected_mode_idx = (self.selected_mode_idx + 1) % len(self.options)
                elif self.step == 1:
                    self.selected_color_idx = (self.selected_color_idx + 1) % len(self.colors)
            elif key in ("\r", "\n"):  # Enter
                self.step += 1

        show_cursor()
        
        # Получаем итоговые настройки
        mode = self.options[self.selected_mode_idx]["value"]
        color_data = self.colors[self.selected_color_idx]
        color = color_data.get("value", "GREEN")
        theme = color_data.get("theme", None)

        return word, mode, color, theme
