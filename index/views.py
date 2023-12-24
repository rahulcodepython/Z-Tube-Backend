from rest_framework import views, response


class Home(views.APIView):
    def get(self, request, format=None):
        return response.Response({'message': 'Ok'})

    def post(self, request, format=None):
        print(request.data)
        return response.Response({'message': 'Ok'})
