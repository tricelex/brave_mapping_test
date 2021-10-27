import re
import time
import requests
import schedule
from pydantic.schema import datetime

from schedule import every, repeat, run_pending
from datetime import datetime
from pydantic import ValidationError

from models import Article


def format_time(time_string: str = None) -> datetime:
    new_time = time_string.replace(';', ':')
    return datetime.fromisoformat(new_time)


def remove_html_tags(text: str) -> str:
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def get_media_section(article_id: int, media_id: int = None) -> list:
    media_url = f'https://mapping-test.fra1.digitaloceanspaces.com/data/media/{article_id}.json'
    med = requests.get(media_url).json()
    item = next(item for item in med if item["id"] == media_id)
    if 'pub_date' in item.keys():
        item['publication_date'] = item.pop('pub_date')
        item['publication_date'] = format_time(item['publication_date'])
    return item


def format_sections(section_list: list, article_id: int) -> list:
    new_sections_list = []
    for x in section_list:
        if (
                'media' in x.values()
                and get_media_section(article_id, x['id']) not in new_sections_list
        ):
            new_sections_list.append(get_media_section(article_id, x['id']))
        for a in x.keys():
            if a == 'text':
                x[a] = remove_html_tags(x[a])
                new_sections_list.append(x)
    return new_sections_list


def read_data():
    list_of_articles = 'https://mapping-test.fra1.digitaloceanspaces.com/data/list.json'

    article_list = requests.get(list_of_articles)
    article_ids = [x['id'] for x in article_list.json()]
    for article_id in article_ids:
        article_link = f'https://mapping-test.fra1.digitaloceanspaces.com/data/articles/{article_id}.json'

        article = requests.get(
            f'https://mapping-test.fra1.digitaloceanspaces.com/data/articles/{article_id}.json').json()
        try:

            output = Article(id=article['id'], original_language=article['original_language'],
                             thumbnail=article['thumbnail'], url=article_link,
                             categories=[article['category']], tags=article['tags'], author=article['author'],
                             publication_date=format_time(article['pub_date']),
                             modification_date=format_time(article['mod_date']),
                             sections=format_sections(article['sections'], article_id)
                             )
            print(output.json())
        except ValidationError as e:
            print(e.json())


schedule.every(5).minutes.do(read_data)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)
