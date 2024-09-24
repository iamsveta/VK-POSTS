import requests
import csv
import datetime

# использую VK API для создания таблицы, нужно ввести токен
access_token = 'Ваш токен'
api_version = '5.131'
owner_id = 'id или короткое имя' # Вк-страница друга
count = 100  # количество постов за один запрос
url = 'https://api.vk.com/method/wall.get'

# создаю для записи CSV-таблица лайков и дат
with open('vk_posts.csv', 'w', newline='', encoding='utf-8') as file:
    fieldnames = ['Дата поста (UTC)', 'Количество лайков']
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    # заголовки таблицы
    writer.writeheader()

    # переменные для постраничного запроса
    offset = 0
    total_posts = 1  # кол-во постов, нужно чтобы начать цикл

    # запрашиваем посты, пока они есть
    while offset < total_posts:
        # параметры запроса
        params = {
            'owner_id': owner_id,
            'access_token': access_token,
            'v': api_version,
            'count': count,
            'offset': offset  # Увеличиваем с каждым циклом
        }

        # запрос к API
        response = requests.get(url, params=params)
        data = response.json()

        if 'response' in data:
            # общее количество постов
            total_posts = data['response']['count']
            posts = data['response']['items']

            # обработка постов и запись в csv-файл
            for post in posts:
                post_date = post['date']  # дата поста в Unix timestamp

                # обрабатываю лайки (проверка на наличие поля 'likes')
                likes_count = post.get('likes', {}).get('count', 0)

                # Unix timestamp в дату UTC
                date_utc = datetime.datetime.fromtimestamp(post_date, datetime.timezone.utc).isoformat().replace("T", " ")

                # удаляю миллисекунды
                date_utc_cleaned = date_utc.split("+")[0]

                #запись в CSV
                writer.writerow({'Дата поста (UTC)': date_utc_cleaned, 'Количество лайков': likes_count})

            # Увеличиваем offset для следующего запроса
            offset += count
        else:
            # сообщение об ошибке, если она есть
            error_message = data.get('error', {}).get('error_msg', 'Неизвестная ошибка')
            print(f"Ошибка: {error_message}")
            break

print("Все посты записаны в vk_posts.csv.")
