from rest_framework import viewsets, serializers

from .models import Pull, Question

class PullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pull
        fields = '___all___'

class PullViewSet(viewsets.ModelViewSet):
    serializer_class = PullSerializer
    queryset = Pull.objects.all()

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '___all___'

class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()