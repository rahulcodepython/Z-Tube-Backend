from djoser.social.views import ProviderAuthView
from . import serializers


class CustomProviderAuthView(ProviderAuthView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return response
