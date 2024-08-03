from rest_framework import views, response


class TestIndex(views.APIView):
    def get(self, request):
        return response.Response({"msg": "Ok! Running..."})
