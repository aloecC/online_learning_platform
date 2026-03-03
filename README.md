||| Шаги для запуска проекта через 
docker-compose:
1. Копирование Dockerfile и Docker-compose.yml
2. Настройка файла .env (Конфиденциальность)
3. Проверка файлов исключений .gitignore и .dockerignore
Первый запуск 
1. docker compose down -v # Остановит и удалит все контейнеры, сети, и ТОМЫ (postgres_data, media)
2. docker compose up -d --build # Запустит все сервисы и соберет образы
*  -d: Запустить в фоновом режиме.
  •  --build: Пересобрать образы (особенно важно после изменений в Dockerfile).
3. docker compose ps # Проверит статус контейнеров(Все сервисы должны быть в статусе Up или Running)
4. docker compose logs -f  # Покажет логи (для отладки)
5. docker compose exec app poetry run python manage.py migrate # Выполнит миграции Django
6. docker compose exec app poetry run python manage.py createsuperuser # Создаст суперпользователя Django
7. Проверьте веб-приложение:
  Откройте браузер и перейдите на http://localhost:8000/. Должна открыться страница Django.
  Проверьте админку: http://localhost:8000/admin/.
8. docker compose logs worker # Проверит Celery Worker



 