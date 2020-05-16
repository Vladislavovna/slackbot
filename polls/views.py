import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets, serializers
import requests
from slack import WebClient

from .models import Poll, Question, SlackUser, QuestionAnswer, PollUserMeta, PollAnswer


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = '__all__'


class PollViewSet(viewsets.ModelViewSet):
    serializer_class = PollSerializer
    queryset = Poll.objects.all()


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.filter(poll=self.kwargs['poll_pk'])


@csrf_exempt
def interactive_hook(request):
    client = WebClient(token=settings.BOT_TOKEN)
    json_dict = json.loads(request.POST['payload'])
    print(json_dict)
    if json_dict['token'] != settings.VERIFICATION_TOKEN:
        return HttpResponse(status=403)

    if json_dict['type'] == 'interactive_message':
        if json_dict['actions'][0]['name'] == 'poll_start':
            poll_id = json_dict['actions'][0]['value']
            poll = Poll.objects.get(id=int(poll_id))

            modal_json = poll.get_modal_json()

            poll_meta = PollUserMeta.objects.get(poll_id=poll_id, slack_user__slack_id=json_dict['user']['id'])
            poll_meta.response_url = json_dict['response_url']
            poll_meta.save()

            r = client.views_open(
                trigger_id=json_dict['trigger_id'],
                view=modal_json
            )
            print(r)
            return HttpResponse(status=200)

    if json_dict['type'] == 'view_submission':
        user, _ = SlackUser.objects.get_or_create(
            slack_id=json_dict['user']['id'],
            username=json_dict['user']['username']
        )
        question_id_to_block_id = dict()

        for x in json_dict['view']['blocks']:
            question_id_to_block_id[x['element']['action_id']] = x['block_id']

        state_data = json_dict['view']['state']['values']
        for k, v in question_id_to_block_id.items():
            answer = state_data[v][k]['value']

            q = Question.objects.get(id=int(k))
            poll_ans, _ = PollAnswer.objects.get_or_create(poll=q.poll, slack_user=user, )
            QuestionAnswer.objects.create(
                poll_answer=poll_ans,
                question_id=int(k),
                answer_text=answer
            )

        poll = Question.objects.get(id=int(next(iter(question_id_to_block_id)))).poll
        poll_meta = PollUserMeta.objects.get(poll=poll, slack_user=user)
        client.chat_update(
            channel=poll_meta.channel,
            ts=poll_meta.entrypoint_message_ts,
            attachments=[{
                "text": f"Ответ на опрос {poll.name} получен",
                "callback_id": user.slack_id + "hr_poll_started" + str(poll.id),
                "color": "#3AA3E3",
                "attachment_type": "default",
            }]
        )
        return HttpResponse(status=200)

    # return the challenge code here
    return HttpResponse(status=500)
