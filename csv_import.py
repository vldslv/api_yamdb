import csv
import os

from api_yamdb import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_yamdb.settings')
import django

django.setup()

DATA_DIR = os.path.join(settings.BASE_DIR, 'data')

from api.models import Category, Comments, Genre, Review, Title
from users.models import User


def user_import():
    with open(os.path.join(DATA_DIR, 'users.csv'), encoding='utf8') as users:
        reader = csv.reader(users)
        u = User
        print(f'Импорт данных для модели User... Сейчас в базе {u.objects.count()} записей')
        for row in reader:
            if row[0] == 'id':
                continue
            u.objects.get_or_create(
                id=row[0],
                username=row[1],
                email=row[2],
                role=row[3],
                bio=row[4],
                first_name=row[5],
                last_name=row[6],
                )
        print(f'Импорт завершён. Записей - {u.objects.count()}')


def category_import():
    with open(os.path.join(DATA_DIR, 'category.csv'), encoding='utf8') as category:
        reader = csv.reader(category)
        c = Category
        print(f'Импорт данных для модели Category... Сейчас в базе {c.objects.count()} записей')
        for row in reader:
            if row[0] == 'id':
                continue
            c.objects.get_or_create(
                id=row[0],
                name=row[1],
                slug=row[2],
                )
        print(f'Импорт завершён. Записей - {c.objects.count()}')


def genre_import():
    with open(os.path.join(DATA_DIR, 'genre.csv'), encoding='utf8') as genre:
        reader = csv.reader(genre)
        g = Genre
        print(f'Импорт данных для модели Genre... Сейчас в базе {g.objects.count()} записей')
        for row in reader:
            if row[0] == 'id':
                continue
            g.objects.get_or_create(
                id=row[0],
                name=row[1],
                slug=row[2],
                )
        print(f'Импорт завершён. Записей - {g.objects.count()}')


def title_import():
    with open(os.path.join(DATA_DIR, 'titles.csv'), encoding='utf8') as titles:
        reader = csv.reader(titles)
        t = Title
        print(f'Импорт данных для модели Title... Сейчас в базе {t.objects.count()} записей')
        for row in reader:
            if row[0] == 'id':
                continue
            t.objects.get_or_create(
                id=row[0],
                name=row[1],
                year=row[2],
                category=Category.objects.get(id=row[3]),
                )
        print(f'Импорт завершён. Записей - {t.objects.count()}')


def genre_title_import():
    with open(os.path.join(DATA_DIR, 'genre_title.csv'), encoding='utf8') as genre_title:
        reader = csv.reader(genre_title)
        print(f'Импорт данных связей Title и Genre')
        for row in reader:
            if row[0] == 'id':
                continue
            t = Title.objects.get(id=row[1])
            g = Genre.objects.get(id=row[2])
            t.genre.add(g)
        print('Импорт завершён')


def review_import():
    with open(os.path.join(DATA_DIR, 'review.csv'), encoding='utf8') as review:
        reader = csv.reader(review)
        r = Review
        print(f'Импорт данных для модели Review... Сейчас в базе {r.objects.count()} записей')
        for row in reader:
            if row[0] == 'id':
                continue
            r.objects.get_or_create(
                id=row[0],
                title=Title.objects.get(id=row[1]),
                text=row[2],
                author=User.objects.get(id=row[3]),
                score=row[4],
                pub_date=row[5],
                )
        print(f'Импорт завершён. Записей - {r.objects.count()}')


def comments_import():
    with open(os.path.join(DATA_DIR, 'comments.csv'), encoding='utf8') as comments:
        reader = csv.reader(comments)
        c = Comments
        print(f'Импорт данных для модели Comments... Сейчас в базе {c.objects.count()} записей')
        for row in reader:
            if row[0] == 'id':
                continue
            c.objects.get_or_create(
                id=row[0],
                review=Review.objects.get(id=row[1]),
                text=row[2],
                author=User.objects.get(id=row[3]),
                pub_date=row[4],
                )
        print(f'Импорт завершён. Записей - {c.objects.count()}')


def main():
    user_import()
    category_import()
    genre_import()
    title_import()
    genre_title_import()
    review_import()
    comments_import()


if __name__ == '__main__':
    main()
