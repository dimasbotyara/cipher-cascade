#!/usr/bin/env python3
import argparse
import os
import sys
from menu import InteractiveMenu
from effects import TextAnimator
from utils import show_cursor, clear_screen

def main():
    parser = argparse.ArgumentParser(description="Cyberpunk Word Waterfall Terminal Animator")
    parser.add_argument("word", nargs="?", help="Слово для анимации (если не указано, откроется меню)")
    parser.add_argument("--mode", choices=["waterfall", "decoder", "matrix", "slide"], default="waterfall", help="Режим анимации")
    parser.add_argument("--color", default="GREEN", help="Базовый цвет (GREEN, CYAN, RED, YELLOW, MAGENTA, ORANGE)")
    parser.add_argument("--theme", choices=["rainbow", "fire", "ice", "neon"], default=None, help="Градиентная тема")
    parser.add_argument("--speed", type=float, default=0.04, help="Скорость анимации (задержка в секундах)")

    args = parser.parse_args()

    if args.word is None:
        menu = InteractiveMenu()
        word, mode, color, theme = menu.run()
        speed = 0.05
    else:
        word = args.word
        mode = args.mode
        color = args.color
        theme = args.theme
        speed = args.speed

    animator = TextAnimator(text=word, speed=speed, color_name=color, theme=theme)

    if mode == "waterfall":
        animator.animate_waterfall()
    elif mode == "decoder":
        animator.animate_decoder()
    elif mode == "matrix":
        animator.animate_matrix()
    elif mode == "slide":
        animator.animate_slide()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Восстанавливаем курсор и терминал
        show_cursor()
        print("\n\n\033[38;5;196m[!] Прервано пользователем (Ctrl+C). До встречи! 👋\033[0m")
        # Мгновенный и чистый выход из процесса ОС без вызова исключений Python
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
