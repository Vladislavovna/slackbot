<<<<<<< HEAD
from rest_framework import viewsets, serializes

class ArticleSerializer(serializes.ModelSerializer)

class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
=======
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
>>>>>>> 327bad21e3d7046bf9211baf7b9a6c5822708dcc
