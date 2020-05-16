import os
import json
from polls.models import SlackUser
from slack import WebClient
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Подгружает список пользователей'

    def handle(self, *args, **options):
        client = WebClient(token='xoxp-1093552724881-1080926571618-1100616862002-94586771c34453bfd2dd0d5090f33080')
        data = client.users_list()

        for member in data['members']:
            if 'email' in member['profile']:
                email = member['profile']['email']
                name = member['profile']['real_name']
                slack_id = member['id']
                SlackUser.objects.get_or_create(username=name, email=email, slack_id=slack_id)
