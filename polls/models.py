from django.db import models


# Create your models here.


class Poll(models.Model):
    name = models.CharField(max_length=20)
    message_text = models.TextField()

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
                        "action_id": "title",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Пожалуй, лучшая точка в этом деле.",
                            "multiline": True
                        }
                    },
                    "label": {
                        "type": "plain_text",
                        "text": x.text,
                        "question_id": x.id
                    }
                }
                for x in questions
            ]
        }
        return slack_modal


class Question(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()


class SlackUser(models.Model):
    slack_id = models.CharField(primary_key=True, max_length=20)
    email = models.TextField(null=True)
    username = models.CharField(max_length=200)


class QuestionAnswer(models.Model):
    question = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='answers')
    slack_user = models.ForeignKey(SlackUser, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.TextField()

