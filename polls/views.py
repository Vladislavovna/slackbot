from rest_framework import viewsets, serializers

from .models import Poll, Question

class PullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = '___all___'

class PullViewSet(viewsets.ModelViewSet):
    serializer_class = PullSerializer
    queryset = Poll.objects.all()

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '___all___'

class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()