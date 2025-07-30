# Описание
Проект YaCut — это сервис укорачивания ссылок. Его назначение — ассоциировать длинную пользовательскую ссылку с короткой, которую предлагает сам пользователь или предоставляет сервис.

Дополнительная функция YaCut — загрузка сразу нескольких файлов на Яндекс Диск и предоставление коротких ссылок пользователю для скачивания этих файлов.

# Установка

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/FantalovSergey/async-yacut.git
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Для Linux/macOS

    ```
    source venv/bin/activate
    ```

* Для Windows

    ```
    venv\Scripts\activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Создать в директории проекта файл .env с четыремя переменными окружения:

```
FLASK_APP=yacut
FLASK_ENV=development
SECRET_KEY=your_secret_key
DB=sqlite:///db.sqlite3
```

Создать базу данных и применить миграции:

```
flask db upgrade
```

Запустить проект:

```
flask run
```

# Запросы к API
Полный список типовых запросов к API и ответов на эти запросы находится в файле openapi.yml.

# Стек
- Python 3.12.7
- Flask
- SQLAlchemy
- pytest-django

# Об авторе
Студент факультета Бэкенд платформы Яндекс.Практикум [Фанталов Сергей](https://github.com/FantalovSergey).
