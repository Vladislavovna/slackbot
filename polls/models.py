from django.db import models
from django.utils.safestring import mark_safe

# Create your models here.
from slack import WebClient

from myproject import settings


class Poll(models.Model):
    name = models.CharField(max_length=20)
    message_text = models.TextField()

    def __str__(self):
        return f'{self.name}/{self.id}'

    def send_poll_starter_to_user(self, slack_user):
        client = WebClient(token=settings.BOT_TOKEN)

        poll_msg = client.chat_postMessage(
            channel=slack_user.slack_id,
            text=self.name,
            attachments=[{
                "text": self.message_text,
                "callback_id": slack_user.slack_id + "hr_poll_started" + str(self.id),
                "color": "#3AA3E3",
                "attachment_type": "default",
                "actions": [{
                    "name": "poll_start",
                    "text": ":new_moon_with_face: Начать",
                    "type": "button",
                    "value": self.id
                }]
            }]
        )
        print(poll_msg)
        PollUserMeta.objects.create(
            slack_user=slack_user,
            poll=self,
            channel=poll_msg['channel'],
            entrypoint_message_ts=poll_msg.data['ts']
        )

    def get_modal_json(self):
        questions = self.questions.all()
        slack_modal = {
            "type": "modal",
            "title": {
                "type": "plain_text",
                "text": f"Опрос {self.name}",
                "emoji": True
            },
            "submit": {
                "type": "plain_text",
                "text": "Submit",
                "emoji": True
            },
            "close": {
                "type": "plain_text",
                "text": "Cancel",
                "emoji": True
            },
            "blocks": [
                {
                    "type": "input",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": str(x.id),
                        "multiline": True,
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Пожалуй, лучшая точка в этом деле.",
                        }
                    },
                    "label": {
                        "type": "plain_text",
                        "text": x.text,
                    }
                }
                for x in questions
            ]
        }
        return slack_modal


class Question(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()

    def __str__(self):
        return f'{self.text}'


class SlackUser(models.Model):
    slack_id = models.CharField(primary_key=True, max_length=20)
    email = models.TextField(null=True)
    username = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.username}/{self.email}'


class PollUserMeta(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    slack_user = models.ForeignKey(SlackUser, on_delete=models.CASCADE)
    entrypoint_message_ts = models.CharField(max_length=100)
    channel = models.TextField(null=True)


class PollAnswer(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    slack_user = models.ForeignKey(SlackUser, on_delete=models.CASCADE, related_name='answers')

    def __str__(self):
        return f'{self.poll.name}/{self.slack_user.username}'


class QuestionAnswer(models.Model):
    poll_answer = models.ForeignKey(PollAnswer, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.TextField()


class PollSchedule(models.Model):
    start_at = models.DateTimeField()
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    slack_user = models.ForeignKey(SlackUser, on_delete=models.CASCADE)
