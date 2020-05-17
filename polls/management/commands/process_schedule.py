from django.core.management.base import BaseCommand
from datetime import datetime
from myproject import settings
from polls import models
from slack import WebClient
from polls.models import PollSchedule


class Command(BaseCommand):
    help = 'Запускает опрос'

    def handle(self, *args, **options):
        tasks = PollSchedule.objects.filter(start_at__lte=datetime.now())
        for task in tasks:
            task.poll.send_poll_starter_to_user(task.slack_user)
            task.delete()
