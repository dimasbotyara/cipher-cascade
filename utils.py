import os
import sys
import atexit
from typing import List, Tuple

# Включаем поддержку ANSI на Windows
if sys.platform == "win32":
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

def clear_screen():
    """Очистка экрана без мерцания."""
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

def move_cursor(x: int, y: int):
    """Перемещение курсора в координаты X, Y (1-based)."""
    sys.stdout.write(f"\033[{y};{x}H")

def hide_cursor():
    """Скрыть курсор."""
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

def show_cursor():
    """Показать курсор и сбросить стили."""
    sys.stdout.write("\033[?25h\033[0m")
    sys.stdout.flush()

# Гарантируем, что курсор вернется, даже если программа вылетит с ошибкой!
atexit.register(show_cursor)

def get_terminal_size() -> Tuple[int, int]:
    """Возвращает (ширина, высота) терминала."""
    try:
        columns, rows = os.get_terminal_size()
        return columns, rows
    except OSError:
        return 80, 24

def get_color_escape(r: int, g: int, b: int, background: bool = False) -> str:
    """Генерация ANSI-кода для RGB цвета."""
    mode = 48 if background else 38
    return f"\033[{mode};2;{r};{g};{b}m"

def interpolate_color(color1: Tuple[int, int, int], color2: Tuple[int, int, int], factor: float) -> Tuple[int, int, int]:
    """Интерполяция между двумя цветами."""
    return (
        int(color1[0] + (color2[0] - color1[0]) * factor),
        int(color1[1] + (color2[1] - color1[1]) * factor),
        int(color1[2] + (color2[2] - color1[2]) * factor),
    )

def generate_gradient(text: str, colors: List[Tuple[int, int, int]]) -> str:
    """Применяет многоцветный градиент к тексту."""
    if not colors or len(text) == 0:
        return text
    if len(colors) == 1:
        return get_color_escape(*colors[0]) + text + "\033[0m"

    result = []
    n = len(text)
    num_segments = len(colors) - 1
    segment_len = n / num_segments if num_segments > 0 else 1

    for i, char in enumerate(text):
        if char == " ":
            result.append(" ")
            continue
        segment = min(int(i / segment_len), num_segments - 1)
        factor = (i - (segment * segment_len)) / segment_len
        r, g, b = interpolate_color(colors[segment], colors[segment + 1], factor)
        result.append(f"{get_color_escape(r, g, b)}{char}")

    result.append("\033[0m")
    return "".join(result)

def get_key() -> str:
    """Считывает одно нажатие клавиши с поддержкой Ctrl+C."""
    if sys.platform == "win32":
        import msvcrt
        ch = msvcrt.getch()
        # Если нажат Ctrl+C
        if ch == b'\x03':
            raise KeyboardInterrupt
        if ch in (b'\x00', b'\xe0'):  # Стрелочки на Windows
            ch2 = msvcrt.getch()
            return f"arrow_{ch2}"
        return ch.decode('utf-8', errors='ignore')
    else:
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            # cbreak режим оставляет сигналы прерывания рабочими
            tty.setcbreak(fd)
            ch = sys.stdin.read(1)
            # Если нажат Ctrl+C (байт \x03)
            if ch == '\x03':
                raise KeyboardInterrupt
            if ch == '\x1b':  # Стрелочки на Unix/Linux
                ch2 = sys.stdin.read(2)
                return f"arrow_{ch2}"
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
