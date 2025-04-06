import os
import random
import time
from django.http import StreamingHttpResponse, HttpResponse
from django.conf import settings
from django.urls import path
from django.core.wsgi import get_wsgi_application
from django.shortcuts import render

# Константа для разделителя кадров
FRAME_SEPARATOR = "--space--"

# Настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', __name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SECRET_KEY = 'your-secret-key-here'
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
INSTALLED_APPS = ['django.contrib.staticfiles']
ROOT_URLCONF = __name__
STATIC_URL = '/static/'
ANIMATIONS_DIR = os.path.join(BASE_DIR, 'animations')
FRAME_HEIGHT = 30  # Высота кадра (должна совпадать с generate_cbo.py)

# Настройка шаблонов
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': False,
    },
]

def generate_chunks(anim_id):
    animation_file = os.path.join(ANIMATIONS_DIR, f"{anim_id}.txt")
    
    if os.path.exists(animation_file):
        with open(animation_file, 'r', encoding='utf-8') as f:
            frames = f.read().split(FRAME_SEPARATOR)
            while True:
                for frame in frames:
                    lines = frame.strip().split('\n')
                    # Добавляем пустые строки сверху, если нужно
                    if len(lines) < FRAME_HEIGHT:
                        lines = [' ' * len(lines[0])] * (FRAME_HEIGHT - len(lines)) + lines
                    # Обрезаем до нужной высоты
                    lines = lines[:FRAME_HEIGHT]
                    # Добавляем полоску внизу
                    lines.append('-' * len(lines[0]))  # Полоска из дефисов
                    padded_frame = '\n'.join(lines)
                    yield f"{padded_frame}\r\n\r\n"
                    time.sleep(0.2)
    else:
        # Текстовый ответ для неверного запроса
        available_animations = [f[:-4] for f in os.listdir(ANIMATIONS_DIR) 
                               if f.endswith('.txt')]
        if available_animations:
            random_anim = random.choice(available_animations)
            message = f"Animation {anim_id}.txt not found.\nTry this one:\ncurl http://localhost:8000/{random_anim}/"
        else:
            message = "Animation not found. No animations available."
        yield message

def stream_animation(request, anim_id="1"):
    animation_file = os.path.join(ANIMATIONS_DIR, f"{anim_id}.txt")
    if os.path.exists(animation_file):
        response = StreamingHttpResponse(
            generate_chunks(anim_id),
            content_type='text/plain; charset=utf-8'
        )
    else:
        response = HttpResponse(
            next(generate_chunks(anim_id)),  # Берем первый (и единственный) элемент из генератора
            content_type='text/plain; charset=utf-8'
        )
    return response

def index(request):
    available_animations = [f[:-4] for f in os.listdir(ANIMATIONS_DIR) 
                           if f.endswith('.txt')]
    return render(request, 'index.jinja2', {'animations': available_animations})

urlpatterns = [
    path('<str:anim_id>/', stream_animation, name='stream_animation'),
    path('', index, name='index'),
]

application = get_wsgi_application()

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    print("Starting server...")
    print("Visit: http://localhost:8000/ for the main page")
    print("Or try: curl http://localhost:8000/1/")
    execute_from_command_line(['', 'runserver', '8000'])