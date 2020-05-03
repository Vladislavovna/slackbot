import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets, serializers
from slack import WebClient

from .models import Poll, Question, SlackUser, QuestionAnswer


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

            client.views_open(
                trigger_id=json_dict['trigger_id'],
                view=modal_json
            )
            return

    if json_dict['type'] == 'view_submission':
        user, _ = SlackUser.objects.get_or_create(
            slack_id=json_dict['user']['id'],
            username=json_dict['user']['username']
        )


    #return the challenge code here
    return HttpResponse(status=500)


