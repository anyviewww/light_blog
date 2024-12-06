# TechnoBlog
Веб-сервис, предназначенный для размещения статей/обьявлений пользователями

## Запуск сервиса
- Необходимо создать python-окружение с зависимостями, указанными в файле requirements.txt
- bash: python3 main.py из директории проекта.

## Открыть openapi.json можно либо через Swagger UI, либо так:
- bash: uvicorn main:app --reload
- открыть http://127.0.0.1:8000/api/docs

## Запуск сервиса при помощи Docker: 
- docker build -t light_blog 
- docker run -d -p 8000:8000 -e DATABASE_URL=postgresql://user:password@localhost/dbname light_blog

  
Сервис будет доступен по адресу 127.0.0.1:8000 (localhost)
