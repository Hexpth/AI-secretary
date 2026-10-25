import json
import os
from flask import Flask, render_template, request
from google import genai

app = Flask(__name__)

# ========== НАСТРОЙКИ ==========
API_KEY = 'AQ.Ab8RN6KtQdWTIMPygwzHzzDH5stghfcgc5x0y_bQlJ5hTgTEQg'
MODEL_NAME = "gemini-3.5-flash"
PROMPT_FILE = "prompt.txt"
# ==============================

client = genai.Client(api_key=API_KEY)

def load_prompt():
    """Читает текст промпта из файла prompt.txt (UTF-8)."""
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        return f.read().strip()

@app.route('/', methods=['GET', 'POST'])
def index():
    answer = None
    error = None

    if request.method == 'POST':
        file = request.files.get('json_file')
        if not file or file.filename == '':
            error = "Выберите JSON-файл"
        elif not file.filename.endswith('.json'):
            error = "Поддерживаются только файлы .json"
        else:
            try:
                # Читаем загруженный JSON
                raw = file.read().decode('utf-8')
                json.loads(raw)  # проверка валидности

                # Читаем промпт из файла и добавляем JSON в конец
                prompt_prefix = load_prompt()
                full_prompt = prompt_prefix + "\n\n" + raw

                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=full_prompt,
                )
                answer = response.text
            except FileNotFoundError:
                error = f"Файл {PROMPT_FILE} не найден рядом с app.py"
            except json.JSONDecodeError:
                error = "Содержимое файла не является валидным JSON"
            except Exception as e:
                error = f"Ошибка при обращении к Gemini: {e}"

    return render_template('index.html', answer=answer, error=error)

if __name__ == '__main__':
    app.run(debug=True, host='10.195.62.145', port=5000)