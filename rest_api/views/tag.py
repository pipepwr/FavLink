from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from rest_api.models import TagsModel, UserURLModel

from django.shortcuts import get_object_or_404


class TagView(APIView):
    """
    API FOR Manage Tag Upon user
    """

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request) -> Response:
        user_object = request.user
        list_result = []
        tag_name = request.GET.get("name")
        if not tag_name:
            tags = TagsModel.objects.filter(user=user_object)

            for tag_object in tags:
                list_url = []
                user_urls_objects = UserURLModel.objects.filter(
                    user=user_object, tags__in=[tag_object]
                )
                for user_urls in user_urls_objects:
                    list_url.append(user_urls.url.url)

                tag_data = {
                    "tag_id": tag_object.id,
                    "tag_name": tag_object.tag,
                    "urls": list_url,
                }
                list_result.append(tag_data)
        else:
            tag_object = TagsModel.objects.filter(tag=tag_name, user=user_object)
            if tag_object:
                # index 0 cause user and tag field is unique_together
                tag_data = {"tag_id": tag_object[0].id, "tag_name": tag_object[0].tag}
                return Response(
                    {"message": "{} Found".format(tag_name), "data": tag_data},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": "Tag Not Found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

        return Response(
            {
                "message": "ALL Tags",
                "data": list_result,
            },
            status=status.HTTP_201_CREATED,
        )

    def post(self, request):

        user_object = request.user
        tag_name = request.data.get("name")
        tag_object, _exists = TagsModel.objects.get_or_create(
            tag=tag_name, user=user_object
        )
        if not _exists:
            return Response(
                {"message": "Tag Already Exists"},
                status=status.HTTP_409_CONFLICT,
            )
        else:
            tag_object.save
            return Response(
                {
                    "message": "Create Tag Complete",
                    "data": tag_object.tag,
                },
                status=status.HTTP_201_CREATED,
            )


class TagViewById(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        user_object = request.user
        tag_object = get_object_or_404(TagsModel, pk=pk, user=user_object)
        if tag_object:
            list_url = []
            user_urls_objects = UserURLModel.objects.filter(
                user=user_object, tags__in=[tag_object]
            )
            for user_urls in user_urls_objects:
                list_url.append(user_urls.url.url)
            return Response(
                {
                    "message": "All Tag",
                    "data": {
                        "tag_id": tag_object.id,
                        "tag_name": tag_object.tag,
                        "urls": list_url,
                    },
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": "Permission Error This URL Not Created by this Tag"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    def delete(self, request, pk):
        user_object = request.user
        tag_object = get_object_or_404(TagsModel, pk=pk, user=user_object)
        if tag_object:
            tag_object.delete()
            tag_object.save()
            return Response({"message": "Deleted"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {"message": "Permission Error This URL Not Created by this Tag"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
