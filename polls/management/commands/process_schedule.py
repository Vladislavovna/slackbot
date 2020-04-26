from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Запускает опрос'

    def handle(self, *args, **options):
        print('Я команда, вызываемая с помощью python manage.py process_schedule')
