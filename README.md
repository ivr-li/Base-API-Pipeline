Микросервис для сбора курсов валют с [exchangerate-api.com](https://www.exchangerate-api.com/) и сохранения в PostgreSQL.

## Структура БД

- **requests** — история запросов к API: id оперпции, базовая валюта, статус API
- **rates** — хранит курсы валют. Связь с таблицей `requests` через `request_id`

## Процесс развертывание через Docker Compose

### 1. Клонировать репозиторий

```bash
git clone https://github.com/ivr-li/Base-API-Pipeline
cd Base-API-Pipeline
```

### 2. Создать `.env` файл

1. Создать файл `.env`
```bash
nano .env
```
2. Скопировать переменные 
```env
API_KEY=your_exchangerate_api_key
DB=postgresql://test_user:1234@db:5432/test_user?sslmode=disable
REQUEST_INTERVAL=60
```

3. Сохранить файл: CTRL+S -> CTRL+X

### 3. Управление контейнером

- Запустить контейнер
```bash
docker-compose up -d --build
```

- Остановить контейнер
```bash
docker-compose down
```

- Удалить данные из БД
```bash
docker-compose down -v
```

## SQL-запрос

- Подключение к БД в контейнере
```bash
docker-compose exec db psql -U test_user -d test_user
```
---
- Получить все курсы валют:
```sql
SELECT 
  requests.id,
  requests.base_code,
	rates.date,
	rates.rate_code,
	rates.rate
FROM 
	requests
JOIN rates
	ON requests.id = rates.request_id
WHERE
  request_status = 'success'
ORDER BY rates.date;
```
