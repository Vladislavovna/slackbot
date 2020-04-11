from rest_framework import viewsets, serializes

class ArticleSerializer(serializes.ModelSerializer)

class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()