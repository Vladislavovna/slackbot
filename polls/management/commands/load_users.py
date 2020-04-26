
"""
Базовый класс для выполнения команд по запуску парсинга
"""

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Подгружает список пользователей'

    def handle(self, *args, **options):
        print('Я команда, вызываемая с помощью python manage.py load_users')
