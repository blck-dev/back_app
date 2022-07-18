from django.http import Http404
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from .serializers import PackageSerializer, SubscriptionSerializer, CreateSubscriptionSerializer
from .models import Tontine, TontineWallet, TontineRound, TontineRules, Penalty, Package, Subscription, CustomFrequency, \
    Rule


class PackageViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    Additionally we also provide an extra `highlight` action.
    """
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,)

    def list(self, request):
        """
        Endpoint to `list` all available packages.
        """
        return Response(self.serializer_class(self.queryset, many=True).data,
                        status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """
        Endpoint to `retrieve` a specific package.
        """
        instance = self.get_object()
        # query = request.GET.get('query', None)  # read extra data
        return Response(self.serializer_class(instance).data,
                        status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        Endpoint to `create` a package. Default values are:
        <br/>
        ```json
        {
        'name': 'Bronze',
        'price': 5000,
        'description': 'No description',
        'point_accorded': 100
        }
        ```
        """
        user = request.user
        print("LOGGED USER ---- ", user)
        print("REQUEST CONTENT --- ", request.data)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubscriptionViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    Additionally we also provide an extra `highlight` action.
    """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (
        permissions.AllowAny,)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return self.serializer_class
        else:
            return CreateSubscriptionSerializer

    def list(self, request):
        """
        Endpoint to `list` all subscriptions.
        """
        return Response(self.serializer_class(self.queryset, many=True).data,
                        status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """
        Endpoint to `retrieve` a specific subscription.
        """
        instance = self.get_object()
        # query = request.GET.get('query', None)  # read extra data
        return Response(self.serializer_class(instance).data,
                        status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        Endpoint to `subscribe` to a package.
        """
        user = request.user
        print("LOGGED USER ---- ", user)

        print("REQUEST CONTENT --- ", request.data)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        endpoint to `revoke` a subscription to a package.
        """
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            pass
        return Response(data={"message": "Subscription to package successfully revoked"}, status=status.HTTP_200_OK)
