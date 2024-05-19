from rest_framework import views, response, status, permissions
from . import serializers, models


def response_bad_request(e):
    return response.Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CreateProductView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            category = (
                models.Category.objects.get(key=request.data["category"])
                if models.Category.objects.filter(key=request.data["category"])
                else None
            )

            if not category:
                return response_bad_request("Category not found")

            subcategory = (
                models.SubCategory.objects.get(key=request.data["subcategory"])
                if models.SubCategory.objects.filter(key=request.data["subcategory"])
                else None
            )

            if not subcategory:
                return response_bad_request("SubCategory not found.")

            if subcategory.category != category:
                return response_bad_request("SubCategory does not referrs to category.")

            serializer = serializers.ProductSerializer(data=request.data)

            if not serializer.is_valid():
                return response_bad_request(serializer.errors)

            serializer.save(
                uploader=request.user, category=category, subcategory=subcategory
            )
            return response.Response({}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return response_bad_request(str(e))


class GetAllMyProductsView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            serializer = serializers.GetAllMyProductsSerializer(
                models.Product.objects.filter(uploader=request.user), many=True
            )
            return response.Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return response_bad_request(str(e))


class EditProductView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, id):
        try:
            product = (
                models.Product.objects.get(id=id)
                if models.Product.objects.filter(id=id)
                else None
            )

            if not product:
                return response_bad_request("Product not found.")

            if product.uploader != request.user:
                return response_bad_request(
                    "You are not allowed to delete this product."
                )

            product.delete()
            return response.Response({}, status=status.HTTP_200_OK)

        except Exception as e:
            return response_bad_request(str(e))
