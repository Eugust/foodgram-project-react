# Приложение Foodgram
[![Django-app workflow](https://github.com/Eugust/foodgram-project-react/actions/workflows/main.yml/badge.svg)](https://github.com/Eugust/foodgram-project-react/actions/workflows/main.yml)

## Описание
Приложение Foodgram - это социальная сеть, в которой пользователи могут выкладывать рецепты блюд, 
просматривать понравившиеся рецепты, добавлять их в избранное, получать список необходимых 
ингредиентов и следить за новыми рецептами понравившиехся пользователей

### Технологии
- django
- djangorestframework
- nginx
- docker
- react
- Yandex.Cloud
- linux


### Запуск проекта в dev-режиме
- Клонировать репозиторий.
- Создать и активировать виртуальное окружение.
- Обновить pip:
```
python3 -m pip install --upgrade pip
``` 
- Переийти в папку backend и установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
``` 
- Выполнить миграции:
```
python3 manage.py migrate
python3 manage.py makemigrations
``` 
- Импортировать тестовые данные:
```
python load_data.py
```
- Запустить docker-compose из папки infra:
```
docker-compose up
```
## Пример работы приложения
См. [Страница Foodgram](http://62.84.120.151/signin)
[Admin](http://62.84.120.151/admin)(username:admin, password:1)

### Автор
- Устинов Евгений
