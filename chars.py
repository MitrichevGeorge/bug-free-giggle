from PIL import Image, ImageDraw, ImageFont
import os
import argparse

# Параметры по умолчанию
FONT_PATH = "C:/Windows/Fonts/consola.ttf"  # Путь к Consolas на Windows
FONT_SIZE = 16  # Размер шрифта в пикселях
CHAR_WIDTH = 10  # Предполагаемая ширина символа в пикселях
CHAR_HEIGHT = 16  # Предполагаемая высота символа в пикселях
CHAR_RANGE = range(32, 232)  # 200 символов от пробела до специальных

def calculate_density(char, font_path, font_size):
    # Создаем изображение чуть больше, чтобы учесть антиалиасинг и отступы
    img = Image.new('L', (CHAR_WIDTH * 2, CHAR_HEIGHT * 2), 255)  # Белый фон
    draw = ImageDraw.Draw(img)
    
    # Загружаем шрифт
    try:
        font = ImageFont.truetype(font_path, font_size)
    except OSError:
        print(f"Ошибка: Не удалось загрузить шрифт {font_path}")
        return 0.0
    
    # Центрируем символ
    bbox = draw.textbbox((0, 0), char, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    offset_x = (CHAR_WIDTH * 2 - text_width) // 2 - bbox[0]
    offset_y = (CHAR_HEIGHT * 2 - text_height) // 2 - bbox[1]
    
    # Рисуем символ черным цветом
    draw.text((offset_x, offset_y), char, font=font, fill=0)
    
    # Обрезаем изображение до реального размера символа
    img = img.crop((CHAR_WIDTH // 2, CHAR_HEIGHT // 2, 
                    CHAR_WIDTH // 2 + CHAR_WIDTH, CHAR_HEIGHT // 2 + CHAR_HEIGHT))
    
    # Подсчитываем плотность с учетом антиалиасинга
    pixels = img.getdata()
    total_pixels = CHAR_WIDTH * CHAR_HEIGHT
    density = sum(1 - pixel / 255 for pixel in pixels) / total_pixels  # Учитываем градации серого
    
    return density

def main():
    # Парсим аргументы командной строки
    parser = argparse.ArgumentParser(description="Calculate character densities for Consolas font")
    parser.add_argument('--font-path', default=FONT_PATH, help="Path to Consolas font file")
    parser.add_argument('--font-size', type=int, default=FONT_SIZE, help="Font size in pixels")
    parser.add_argument('--start', type=int, default=32, help="Start of character range")
    parser.add_argument('--end', type=int, default=232, help="End of character range (exclusive)")
    args = parser.parse_args()

    font_path = args.font_path
    font_size = args.font_size
    char_range = range(args.start, args.end)

    # Проверяем наличие шрифта
    if not os.path.exists(font_path):
        print(f"Ошибка: шрифт {font_path} не найден. Укажите правильный путь с помощью --font-path.")
        return
    
    # Словарь для хранения плотностей
    densities = {}
    
    # Обрабатываем символы
    for code in char_range:
        char = chr(code)
        density = calculate_density(char, font_path, font_size)
        densities[char] = density
    
    # Сортируем по плотности
    sorted_densities = sorted(densities.items(), key=lambda x: x[1])
    
    # Выводим в консоль
    print(f"Плотности символов для шрифта Consolas (размер {font_size}px):")
    print("{:<5} {:<10} {}".format("Символ", "Код", "Плотность"))
    print("-" * 30)
    for char, density in sorted_densities:
        print("{:<5} {:<10} {:.4f}".format(repr(char), ord(char), density))
    
    # Форматируем для dict.txt
    dict_content = "CHAR_DENSITIES = {\n"
    for char, density in sorted_densities:
        dict_content += f"    '{char}': {density:.4f},\n"
    dict_content = dict_content.rstrip(",\n") + "\n}"
    
    # Сохраняем в dict.txt
    with open("dict.txt", "w", encoding="utf-8") as f:
        f.write(dict_content)
    print("\nСловарь плотностей сохранен в dict.txt в формате для рендерера")

if __name__ == "__main__":
    main()