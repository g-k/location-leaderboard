from django.conf import settings
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from leaderboard.fxa.authenticator import OAuthTokenAuthentication
from leaderboard.contributors.models import Contributor
from leaderboard.contributors.permissions import (
    AccessTokenContributorPermission,
)
from leaderboard.contributors.serializers import (
    ContributionSerializer,
    ContributorUpdateSerializer,
)


class ContributionsConfigView(APIView):

    def get(self, request):
        config_data = {
            'tile_size': settings.CONTRIBUTION_TILE_SIZE,
            'record_duration': settings.CONTRIBUTION_RECORD_DURATION,
        }
        return Response(config_data, content_type='application/json')


class UpdateContributorView(UpdateAPIView):
    queryset = Contributor.objects.all()
    authentication_classes = (OAuthTokenAuthentication,)
    permission_classes = (AccessTokenContributorPermission,)
    serializer_class = ContributorUpdateSerializer
    lookup_field = 'uid'


class CreateContributionsView(CreateAPIView):
    """
    Create a contribution from user submitted data.
    """
    authentication_classes = (OAuthTokenAuthentication,)
    serializer_class = ContributionSerializer

    def get_serializer(self, data=None, *args, **kwargs):
        if data:
            data = data.get('items', [])

        return super(CreateContributionsView, self).get_serializer(
            data=data, many=True, *args, **kwargs)
