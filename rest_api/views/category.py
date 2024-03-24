from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from rest_api.models import CategoriesModel, UserURLModel

from django.shortcuts import get_object_or_404


class CategoryView(APIView):
    """
    API FOR Manage Category Upon user
    """

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_object = request.user
        list_result = []
        category_name = request.GET.get("name")
        if not category_name:
            catagories = CategoriesModel.objects.filter(user=user_object)
            for category_object in catagories:
                category_data = {
                    "category_id": category_object.id,
                    "category_name": category_object.category,
                }
                list_result.append(category_data)

        else:
            category_objects = CategoriesModel.objects.filter(
                category=category_name, user=user_object
            )
            if category_objects:
                category_data = {
                    "category_id": category_objects[0].id,
                    "category_name": category_objects[0].category,
                }
                return Response(
                    {
                        "message": "{} Found".format(category_name),
                        "data": category_data,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": "Category Not Found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

        return Response(
            {
                "message": "ALL Category",
                "data": list_result,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):

        user_object = request.user
        category_name = request.data.get("name")
        category_object, _exists = CategoriesModel.objects.get_or_create(
            category=category_name, user=user_object
        )
        if not _exists:
            return Response(
                {"message": "Category Already Exists"},
                status=status.HTTP_409_CONFLICT,
            )
        else:
            category_object.save
            return Response(
                {
                    "message": "Create Category Complete",
                    "data": category_object.category,
                },
                status=status.HTTP_201_CREATED,
            )


class CategoryViewById(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        user_object = request.user
        category_object = get_object_or_404(CategoriesModel, pk=pk, user=user_object)
        if category_object:
            list_url = []
            user_urls_objects = UserURLModel.objects.filter(
                user=user_object, category=category_object
            )
            for user_urls in user_urls_objects:
                list_url.append(user_urls.url.url)
            return Response(
                {
                    "message": "All Category",
                    "data": {
                        "category_id": category_object.id,
                        "category_name": category_object.category,
                        "urls": list_url,
                    },
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": "Permission Error This URL Not Created by this category"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    def delete(self, request, pk):
        user_object = request.user
        category_object = get_object_or_404(CategoriesModel, pk=pk, user=user_object)
        if category_object:
            category_object.delete()
            category_object.save()
            return Response({"message": "Deleted"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {"message": "Permission Error This URL Not Created by this category"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
