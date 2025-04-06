import os
import math
import time
import sys
import argparse

ANIMATIONS_DIR = "animations"
FRAME_SEPARATOR = "--space--"
TOP_PADDING = 5  # Количество пустых строк сверху

# Константы параметров по умолчанию
ROTATION_AXES = {'x': 0, 'y': 1, 'z': 0.0}  # Оси вращения и их скорости
START_ROTATION = [0, 0.0, 180.0]  # Начальный поворот [x, y, z] в градусах
LIGHTS = [([0, 0, 10], 1.0)]  # Список источников света: ([x, y, z], яркость)
FRAME_WIDTH = 80
FRAME_HEIGHT = 30
FIXED_BOTTOM_OFFSET = 1  # Расстояние от нижней границы кадра до низа объекта

# Плотности символов из вашего примера
CHAR_DENSITIES = {
    ' ': 0.0000, ' ': 0.0000, '¸': 0.0159, '`': 0.0208, '´': 0.0208, '·': 0.0248,
    '.': 0.0249, '¯': 0.0256, '-': 0.0292, '­': 0.0292, '¨': 0.0338, '\'': 0.0391,
    ':': 0.0457, '_': 0.0550, ',': 0.0572, '¬': 0.0584, '~': 0.0725, '^': 0.0726,
    '"': 0.0754, ';': 0.0801, '¡': 0.0819, '=': 0.0841, '°': 0.0901, '!': 0.0909,
    '>': 0.0943, '<': 0.0943, '«': 0.0953, '»': 0.0966, '+': 0.0972, '³': 0.0987,
    '¹': 0.0988, '¿': 0.1026, 'c': 0.1031, '¦': 0.1042, 'r': 0.1051, '/': 0.1054,
    '\\': 0.1055, '²': 0.1078, '?': 0.1100, 'z': 0.1119, '×': 0.1126, '*': 0.1133,
    'v': 0.1151, 'L': 0.1159, 's': 0.1202, 'ç': 0.1207, 'º': 0.1237, 'T': 0.1258,
    'i': 0.1260, '7': 0.1263, '|': 0.1282, 'ª': 0.1283, ')': 0.1300, 'J': 0.1301,
    '(': 0.1302, 'x': 0.1306, 't': 0.1362, 'n': 0.1378, 'u': 0.1381, '}': 0.1395,
    'l': 0.1399, '{': 0.1402, 'C': 0.1403, 'F': 0.1417, 'o': 0.1421, '1': 0.1435,
    '±': 0.1444, 'y': 0.1444, 'Y': 0.1450, '[': 0.1454, 'I': 0.1468, ']': 0.1468,
    '3': 0.1476, 'f': 0.1482, 'j': 0.1485, 'Z': 0.1499, 'e': 0.1525, 'a': 0.1529,
    '5': 0.1537, '2': 0.1546, 'Ç': 0.1551, 'w': 0.1557, 'S': 0.1592, 'Ý': 0.1659,
    'Í': 0.1678, 'Ì': 0.1678, 'E': 0.1688, '£': 0.1707, 'k': 0.1707, 'h': 0.1722,
    '¤': 0.1724, 'P': 0.1725, 'µ': 0.1727, '®': 0.1731, 'à': 0.1737, 'á': 0.1738,
    'V': 0.1776, 'Ï': 0.1786, 'Þ': 0.1794, 'Î': 0.1796, 'q': 0.1798, 'p': 0.1806,
    '6': 0.1808, 'K': 0.1821, 'm': 0.1827, 'U': 0.1831, '9': 0.1833, 'â': 0.1839,
    '4': 0.1855, 'b': 0.1855, 'G': 0.1865, 'ä': 0.1867, 'd': 0.1879, 'É': 0.1897,
    'È': 0.1897, 'ã': 0.1913, 'æ': 0.1930, 'å': 0.1939, '¢': 0.1946, '¥': 0.1984,
    'X': 0.1991, 'A': 0.1993, 'O': 0.1996, 'Ë': 0.2005, '¼': 0.2007, '½': 0.2009,
    'H': 0.2010, 'Ê': 0.2015, 'R': 0.2026, 'Ú': 0.2040, 'Ù': 0.2041, 'D': 0.2113,
    '#': 0.2118, '': 0.2148, '': 0.2148, '': 0.2148, '': 0.2148, '': 0.2148,
    '': 0.2148, '': 0.2148, '': 0.2148, '': 0.2148, '': 0.2148, '': 0.2148,
    '': 0.2148, '': 0.2148, '': 0.2148, '': 0.2148, '': 0.2148, '': 0.2148,
    '': 0.2148, '': 0.2148, '': 0.2148, '': 0.2148, '': 0.2148, '': 0.2148,
    '': 0.2148, '': 0.2148, '': 0.2148, '': 0.2148, '': 0.2148, '': 0.2148,
    '': 0.2148, '': 0.2148, '': 0.2148, '': 0.2148, 'Ü': 0.2148, '¾': 0.2149,
    '8': 0.2154, 'Û': 0.2159, 'ß': 0.2183, '§': 0.2201, 'Á': 0.2202, 'À': 0.2203,
    'Ó': 0.2206, 'Ò': 0.2206, 'Æ': 0.2216, 'N': 0.2216, '0': 0.2231, 'Ð': 0.2264,
    'M': 0.2278, 'B': 0.2279, 'W': 0.2299, 'Ä': 0.2310, 'Ö': 0.2314, 'Â': 0.2321,
    'Ô': 0.2324, '©': 0.2335, '$': 0.2348, 'g': 0.2357, 'Ã': 0.2377, 'Õ': 0.2380,
    'Å': 0.2384, '%': 0.2389, 'Q': 0.2418, '&': 0.2544, 'Ñ': 0.2600, 'Ø': 0.2822,
    '¶': 0.2916, '@': 0.3090
}

def load_obj_file(filename):
    vertices = []
    faces = []
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('v '):
                parts = line.split()
                vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])
            elif line.startswith('f '):
                parts = line.split()
                faces.append([int(p.split('/')[0]) - 1 for p in parts[1:]])
    return vertices, faces

def rotate_point(point, angles):
    x, y, z = point
    cos_x, sin_x = math.cos(angles['x']), math.sin(angles['x'])
    y, z = y * cos_x - z * sin_x, y * sin_x + z * cos_x
    cos_y, sin_y = math.cos(angles['y']), math.sin(angles['y'])
    x, z = x * cos_y + z * sin_y, -x * sin_y + z * cos_y
    cos_z, sin_z = math.cos(angles['z']), math.sin(angles['z'])
    x, y = x * cos_z - y * sin_z, x * sin_z + y * cos_z
    return [x, y, z]

def calculate_lighting(nx, ny, nz, lights):
    intensity = 0
    for light_pos, light_brightness in lights:
        lx, ly, lz = light_pos[0] - nx, light_pos[1] - ny, light_pos[2] - nz
        light_dist = math.sqrt(lx*lx + ly*ly + lz*lz)
        if light_dist == 0:
            continue
        lx, ly, lz = lx/light_dist, ly/light_dist, lz/light_dist
        diffuse = max(0, nx*lx + ny*ly + nz*lz) * light_brightness * 0.7  # Уменьшаем диффузный вклад
        view_z = 1
        hx, hy, hz = lx, ly, lz + view_z
        h_norm = math.sqrt(hx*hx + hy*hy + hz*hz)
        if h_norm > 0:
            hx, hy, hz = hx/h_norm, hy/h_norm, hz/h_norm
        specular = max(0, nx*hx + ny*hy + nz*hz) ** 32 * 0.5 * light_brightness  # Уменьшаем блики
        intensity += diffuse + specular  # Убираем базовую яркость (было 0.2)
    return min(1.0, max(0, intensity))

def get_bounds(vertices):
    min_x = min(v[0] for v in vertices)
    max_x = max(v[0] for v in vertices)
    min_y = min(v[1] for v in vertices)
    max_y = max(v[1] for v in vertices)
    min_z = min(v[2] for v in vertices)
    max_z = max(v[2] for v in vertices)
    return min_x, max_x, min_y, max_y, min_z, max_z

def intensity_to_char(intensity):
    # Выбираем символ с ближайшей плотностью
    closest_char = min(CHAR_DENSITIES.items(), key=lambda x: abs(x[1] - intensity))
    return closest_char[0]

def generate_frame(angle, vertices, faces, axes, start_rotation, lights, width=FRAME_WIDTH, height=FRAME_HEIGHT):
    frame = [[' ' for _ in range(width)] for _ in range(height)]
    z_buffer = [[float('-inf') for _ in range(width)] for _ in range(height)]
    
    # Преобразуем начальный поворот из градусов в радианы
    start_rotation_rad = [math.radians(angle_deg) for angle_deg in start_rotation]
    
    # Комбинируем начальный поворот с анимацией
    angles = {
        'x': start_rotation_rad[0] + angle * axes.get('x', 0.0),
        'y': start_rotation_rad[1] + angle * axes.get('y', 0.0),
        'z': start_rotation_rad[2] + angle * axes.get('z', 0.0)
    }
    rotated_vertices = [rotate_point(v, angles) for v in vertices]
    
    # Определяем границы объекта
    min_x, max_x, min_y, max_y, min_z, max_z = get_bounds(rotated_vertices)
    obj_width = max_x - min_x
    obj_height = max_y - min_y
    
    # Автоматический масштаб
    scale_x = (width - 2) / obj_width if obj_width > 0 else 1
    scale_y = (height - 2 - FIXED_BOTTOM_OFFSET) / obj_height if obj_height > 0 else 1
    scale = min(scale_x, scale_y) or 1
    
    # Фиксируем нижнюю границу объекта
    offset_x = (width - obj_width * scale) / 2 - min_x * scale
    offset_y = height - FIXED_BOTTOM_OFFSET - obj_height * scale - min_y * scale
    
    # Отрисовка граней
    for face in faces:
        v0, v1, v2 = [rotated_vertices[i] for i in face[:3]]
        u = [v1[i] - v0[i] for i in range(3)]
        v = [v2[i] - v0[i] for i in range(3)]
        nx = u[1] * v[2] - u[2] * v[1]
        ny = u[2] * v[0] - u[0] * v[2]
        nz = u[0] * v[1] - u[1] * v[0]
        norm = math.sqrt(nx*nx + ny*ny + nz*nz)
        if norm > 0:
            nx, ny, nz = nx/norm, ny/norm, nz/norm
        
        if nz <= 0:
            continue
        
        x0, y0, z0 = v0
        x1, y1, z1 = v1
        x2, y2, z2 = v2
        px0 = int(x0 * scale + offset_x)
        py0 = int(y0 * scale + offset_y)
        px1 = int(x1 * scale + offset_x)
        py1 = int(y1 * scale + offset_y)
        px2 = int(x2 * scale + offset_x)
        py2 = int(y2 * scale + offset_y)
        
        min_x = max(0, min(px0, px1, px2))
        max_x = min(width - 1, max(px0, px1, px2))
        min_y = max(0, min(py0, py1, py2))
        max_y = min(height - 1, max(py0, py1, py2))
        
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                denom = ((px1 - px2) * (py0 - py2) - (py1 - py2) * (px0 - px2))
                if denom == 0:
                    continue
                w0 = ((px1 - px2) * (y - py2) - (py1 - py2) * (x - px2)) / denom
                w1 = ((px2 - px0) * (y - py0) - (py2 - py0) * (x - px0)) / \
                     ((px2 - px0) * (py1 - py0) - (py2 - py0) * (px1 - px0))
                w2 = 1 - w0 - w1
                
                if w0 >= 0 and w1 >= 0 and w2 >= 0:
                    z = w0 * z0 + w1 * z1 + w2 * z2
                    if z > z_buffer[y][x]:
                        z_buffer[y][x] = z
                        intensity = calculate_lighting(nx, ny, nz, lights)
                        frame[y][x] = intensity_to_char(intensity)
    
    # Преобразуем кадр в строки
    frame_lines = [''.join(row) for row in frame]
    max_frame_height = FRAME_HEIGHT + FIXED_BOTTOM_OFFSET
    
    # Добавляем пустые строки сверху
    frame_lines = [' ' * width] * TOP_PADDING + frame_lines
    
    # Добавляем пустые строки внизу до максимальной высоты
    current_height = len(frame_lines)
    if current_height < max_frame_height + TOP_PADDING:
        frame_lines += [' ' * width] * (max_frame_height + TOP_PADDING - current_height)
    
    return '\n'.join(frame_lines)

def preview_animation(frames):
    print("Full Animation Preview (simulating curl output):")
    for frame in frames:
        sys.stdout.write(frame + "\r\n\r\n")
        sys.stdout.flush()
        time.sleep(0.2)
    print("Preview completed.")

def generate_animation(input_file, output_file, axes=ROTATION_AXES, start_rotation=START_ROTATION, lights=LIGHTS):
    vertices, faces = load_obj_file(input_file)
    if not vertices or not faces:
        print(f"Error: Input file '{input_file}' is empty or invalid.")
        return
    
    frames = []
    steps = 36
    angle_step = math.pi / 18
    
    for i in range(steps):
        angle = i * angle_step
        frame = generate_frame(angle, vertices, faces, axes, start_rotation, lights)
        frames.append(frame)
    
    preview_animation(frames)
    
    if not os.path.exists(ANIMATIONS_DIR):
        os.makedirs(ANIMATIONS_DIR)
    
    output_path = os.path.join(ANIMATIONS_DIR, output_file)
    with open(output_path, "w", encoding='utf-8') as f:
        f.write(FRAME_SEPARATOR.join(frames))
    print(f"Animation generated in {output_path}")
    print(f"Run server.py and try: curl http://localhost:8000/{os.path.splitext(output_file)[0]}/")

def main():
    parser = argparse.ArgumentParser(description="Generate ASCII animation from OBJ file")
    parser.add_argument('--input', default='model.obj', help="Input OBJ file")
    parser.add_argument('--output', default='z.txt', help="Output animation file")
    args = parser.parse_args()
    
    generate_animation(args.input, args.output)

if __name__ == "__main__":
    main()