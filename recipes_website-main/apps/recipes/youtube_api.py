import googleapiclient.discovery as yt_api
import random


def scrape_youtube_videos(q):
    if not q:
        key_words = [
            "Борщ", "Вареники", "Голубці", "Деруни", "Сало з часником",
            "Літні салати", "Осінні супи", "Зимові гарячі напої", "Весняні десерти",
            "Рецепти на Різдво", "Пасхальні кулічі", "Страви на Масницю", "Угощення на Геловін",
            "Вегетаріанські рецепти", "Страви для схуднення", "Сироїдні страви", "Безглютенові рецепти",
            "Сніданки за 5 хвилин", "Обіди за 10 хвилин", "Вечері за 15 хвилин",
            "Як правильно замаринувати м'ясо", "Секрети ідеального тіста", "Як зберегти свіжість овочів",
            "Закарпатська кухня", "Страви Галичини", "Кухня Донбасу", "Львівські угощення",
            "Український стріт-фуд", "Гастромаркети України",
            "Домашні наливки", "Узвар", "Квас",
            "Українські пироги", "Домашні торти", "Рецепти печива"
        ]

        key_word = random.choice(key_words)
        q = key_word
    elif not 'рецепт' in q.lower():
        q = f"Рецепт {q}"

    youtube = yt_api.build('youtube', 'v3', developerKey='AIzaSyCJUcq4p69xwn6q9D1d8Ws2qOjIy_pgskQ')

    request = youtube.search().list(
        q=q,
        part='snippet',
        type='video',
        maxResults=18,
        regionCode='UA'
    )

    response = request.execute()

    videos = []

    for item in response['items']:
        videos.append({
            'title': item['snippet']['title'],
            'description': item['snippet']['description'],
            'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}",
            'thumbnail_url': item['snippet']['thumbnails']['medium']['url']
        })

    return videos
