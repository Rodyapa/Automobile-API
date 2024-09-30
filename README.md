# Automobile-API (Тестовое задание)
## Endpoints
* /api/docs/swagger/ - Документация эндпоинтов.
## Просмотр проекта на локальной машине:
Склонировать репозиторий на локальную машину:
```
git clone git@github.com:Rodyapa/Automobile-API.git
```
Перейти в директорию с кодом бекенда
```
cd Automobile-API/backend
```
Создать виртуальное окружение
```
python3 -m vevn venv 
```
Активировать виртуальное окружение
```
source venv/bin/activate
```
Установить пакетный менеджер Poetry: https://python-poetry.org/docs/
Установить зависимости
```
poetry install 
```
Или установите зависимости с помощью pip
```
pip install -r requirements.txt
```

Собрать статику
```
python automobile_api/manage.py collectstatic
```
Провести миграции
```
python automobile_api/manage.py makemigrations
python automobile_api/manage.py migrate
```
Опционально - создать тестовые записи
```
python manage.py load_test_data_from_csv
```
Запустить локальный сервер
```
python manage.py runserver
```

## Технологии:
    *Python
    *Django
    *Django REST framework
    *Poetry
    *Unittest library 