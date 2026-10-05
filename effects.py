import random
import time
import sys
from config import ALPHABETS, COLORS, GRADIENTS
from utils import (
    clear_screen, move_cursor, get_terminal_size, 
    generate_gradient, hide_cursor, show_cursor
)

class TextAnimator:
    def __init__(self, text: str, speed: float = 0.05, color_name: str = "GREEN", theme: str = None):
        self.text = text
        self.speed = speed
        self.color_name = color_name.upper()
        self.color_code = COLORS.get(self.color_name, COLORS["GREEN"])
        self.theme_colors = GRADIENTS.get(theme) if theme else None
        self.alphabet = ALPHABETS["standard"]

    def _colorize(self, text: str) -> str:
        """Вспомогательный метод окраски."""
        if self.theme_colors:
            return generate_gradient(text, self.theme_colors)
        return f"{self.color_code}{text}{COLORS['RESET']}"

    def animate_waterfall(self):
        """Оригинальный водопад (улучшенный)."""
        hide_cursor()
        clear_screen()
        cols, rows = get_terminal_size()
        
        # Центрирование по вертикали
        start_y = rows // 2
        result = ""
        
        for i, char in enumerate(self.text):
            found = False
            for alpha in self.alphabet:
                current_line = result + alpha
                # Центрируем текст по горизонтали
                padding = " " * ((cols - len(self.text)) // 2)
                
                move_cursor(1, start_y)
                # Очищаем строку и пишем
                sys.stdout.write("\033[K" + padding + self._colorize(current_line) + "\n")
                sys.stdout.flush()
                time.sleep(self.speed * 0.5)

                if alpha == char:
                    result += alpha
                    found = True
                    break
            
            if not found:
                result += char

        # Финальное мигание готового текста
        for _ in range(3):
            move_cursor(1, start_y)
            sys.stdout.write("\033[K" + padding + self._colorize(result) + "\n")
            sys.stdout.flush()
            time.sleep(0.3)
            move_cursor(1, start_y)
            sys.stdout.write("\033[K" + padding + result + "\n")
            sys.stdout.flush()
            time.sleep(0.3)
            
        show_cursor()

    def animate_decoder(self):
        """Эффект дешифратора (символы подбираются случайно и фиксируются)."""
        hide_cursor()
        clear_screen()
        cols, rows = get_terminal_size()
        start_y = rows // 2
        padding = " " * ((cols - len(self.text)) // 2)
        
        current = [" "] * len(self.text)
        locked = [False] * len(self.text)
        
        # Шаг анимации
        for cycle in range(len(self.text) * 4):  # Длина анимации зависит от длины слова
            for i in range(len(self.text)):
                if not locked[i]:
                    current[i] = random.choice(self.alphabet)
            
            # Рандомно фиксируем символы слева направо или случайно
            idx_to_lock = cycle // 4
            if idx_to_lock < len(self.text):
                current[idx_to_lock] = self.text[idx_to_lock]
                locked[idx_to_lock] = True

            output = "".join(current)
            move_cursor(1, start_y)
            sys.stdout.write("\033[K" + padding + self._colorize(output))
            sys.stdout.flush()
            time.sleep(self.speed)
            
            if all(locked):
                break
                
        # На всякий случай выводим оригинал
        move_cursor(1, start_y)
        sys.stdout.write("\033[K" + padding + self._colorize(self.text) + "\n")
        show_cursor()

    def animate_matrix(self):
        """Полноценный зеленый дождь Матрицы с проявлением слова."""
        hide_cursor()
        clear_screen()
        cols, rows = get_terminal_size()
        
        # Текст по центру
        text_len = len(self.text)
        start_x = (cols - text_len) // 2
        start_y = rows // 2
        
        # Массив «капель» дождя: [текущая_строка, скорость, длина_шлейфа]
        columns = [None] * cols
        matrix_alphabet = ALPHABETS["matrix"]
        
        # Карта маски для вывода нашего слова
        word_mask = {}
        for idx, char in enumerate(self.text):
            word_mask[(start_x + idx, start_y)] = char

        frames = 80  # Сколько кадров крутить анимацию
        revealed = set()

        for frame in range(frames):
            # Рандомим появление капель
            for col in range(cols):
                if columns[col] is None:
                    if random.random() < 0.05:
                        columns[col] = {
                            "y": 0,
                            "speed": random.randint(1, 2),
                            "len": random.randint(5, 15)
                        }
                else:
                    # Двигаем каплю
                    columns[col]["y"] += columns[col]["speed"]
                    if columns[col]["y"] >= rows:
                        columns[col] = None  # Сброс капли

            # Рендерим кадр
            for col in range(cols):
                drop = columns[col]
                if drop:
                    y_pos = int(drop["y"])
                    for offset in range(drop["len"]):
                        curr_y = y_pos - offset
                        if 0 <= curr_y < rows:
                            # Проверяем, не наезжает ли капля на наше секретное слово
                            if (col, curr_y) in word_mask:
                                # С шансом открываем букву слова навсегда
                                if frame > frames // 3 and random.random() < 0.1:
                                    revealed.add((col, curr_y))
                            
                            move_cursor(col + 1, curr_y + 1)
                            char = random.choice(matrix_alphabet)
                            
                            # Первый символ капли белый и яркий
                            if offset == 0:
                                sys.stdout.write(f"{COLORS['WHITE']}{char}")
                            elif offset < drop["len"] // 2:
                                sys.stdout.write(f"{COLORS['GREEN']}{char}")
                            else:
                                # Тускло-зеленый хвост
                                sys.stdout.write(f"\033[38;5;22m{char}")

            # Отрисовываем проявленные буквы нашего слова
            for (wx, wy), char in word_mask.items():
                move_cursor(wx + 1, wy + 1)
                if (wx, wy) in revealed or frame > frames - 15:
                    sys.stdout.write(self._colorize(char))
                else:
                    # Если еще не открыли, пишем случайный тусклый символ
                    if random.random() < 0.3:
                        sys.stdout.write(f"\033[38;5;28m{random.choice(matrix_alphabet)}")

            sys.stdout.flush()
            time.sleep(0.04)
            
            # Стираем старый кадр (быстро перерисовывая пустоту)
            if frame < frames - 1:
                clear_screen()
                
        # В конце очищаем экран и оставляем только финальное слово красивым
        clear_screen()
        move_cursor(start_x + 1, start_y + 1)
        sys.stdout.write(self._colorize(self.text) + "\n\n")
        show_cursor()

    def animate_slide(self):
        """Цветной слайд-эффект."""
        hide_cursor()
        clear_screen()
        cols, rows = get_terminal_size()
        start_y = rows // 2
        
        target_padding = (cols - len(self.text)) // 2
        
        for i in range(cols - len(self.text) - target_padding):
            move_cursor(1, start_y)
            current_padding = " " * i
            sys.stdout.write("\033[K" + current_padding + self._colorize(self.text))
            sys.stdout.flush()
            time.sleep(self.speed * 0.3)
            
        move_cursor(1, start_y)
        sys.stdout.write("\033[K" + " " * target_padding + self._colorize(self.text) + "\n")
        show_cursor()
