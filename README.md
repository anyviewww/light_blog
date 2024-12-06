# TechnoBlog
Веб-сервис, предназначенный для размещения статей/обьявлений пользователями

## Запуск сервиса
- Необходимо создать python-окружение с зависимостями, указанными в файле requirements.txt
- bash: python3 main.py из директории проекта.

## Запуск сервиса при помощи docker-compose: 
- docker-compose up --build

## Как открыть схему взаимодействия с сервисом :
- bash: uvicorn main:app --reload
- открыть http://127.0.0.1:8000/api/docs
  Либо через Swagger UI (файл openapi.json)

Сервис будет доступен по адресу 127.0.0.1:8000 (localhost)

