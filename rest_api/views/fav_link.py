from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from rest_api.models import URLModel, TagsModel, CategoriesModel, UserURLModel

import requests
from bs4 import BeautifulSoup as bs

"""
Authetication process
    I'm following this article
    https://www.django-rest-framework.org/api-guide/authentication/#sessionauthentication
"""


class FavLinkView(APIView):
    """
    API FOR Create Favorite URL Upon use and GET all url created by current user
    """

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        list_result = []
        user_url_objects = UserURLModel.objects.all()

        for user_url_object in user_url_objects:
            list_tags = []
            if user_url_object.tags:
                for tag in user_url_object.tags.all():
                    list_tags.append(tag.tag)

            result = {
                "id": user_url_object.id,
                "url": user_url_object.url.url,
                "title": user_url_object.url.title,
                "category": (
                    user_url_object.category.category
                    if user_url_object.category
                    else None
                ),
                "tags": list_tags,
            }

            list_result.append(result)

        return Response(list_result, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Add New Favorite Link
        """

        user_object = request.user
        url = request.data.get("url")
        category = request.data.get("category")
        tags = request.data.get("tags")

        try:
            """
            beatifulsoup: https://www.tutorialspoint.com/extract-the-title-from-a-webpage-using-python
            web scapper
            """

            response = requests.get(url)
            status_code = response.status_code
            soup = bs(response.content, "html.parser")
            title = soup.title.string

        except:
            return Response(
                {"URL Wrong": "Please send Valid Url"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        url_object, _exists = URLModel.objects.get_or_create(
            url=url, user=user_object, title=title, status_code=status_code
        )

        result = {"url": url_object.url, "category": None, "tags": []}

        user_url_object, user_url_exists = UserURLModel.objects.get_or_create(
            user=user_object, url=url_object
        )
        if not user_url_exists:
            return Response(
                {"URL Exists": "Please update url by PUT Route"},
                status=status.HTTP_409_CONFLICT,
            )

        if category:
            category_object, _exists = CategoriesModel.objects.get_or_create(
                category=category, user=user_object
            )
            user_url_object.category = category_object
            result["category"] = user_url_object.category.category

        if tags:
            list_tags = []
            for tag in tags:
                tags_object, _exists = TagsModel.objects.get_or_create(
                    tag=tag, user=user_object
                )
                list_tags.append(tags_object.tag)
                user_url_object.tags.add(tags_object)
            result["tags"] = list_tags

        user_url_object.save()

        return Response({"Create Sucessful": result}, status=status.HTTP_201_CREATED)


class FavLinkViewById(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):

        user_object = request.user
        user_url_object = get_object_or_404(UserURLModel, pk=pk)

        if user_url_object.user == user_object:
            list_tags = []
            result = {
                "id": user_url_object.id,
                "url": user_url_object.url.url,
                "title": user_url_object.url.title,
                "category": (
                    user_url_object.category.category
                    if user_url_object.category
                    else None
                ),
            }
            if user_url_object.tags:
                for tag in user_url_object.tags.all():
                    list_tags.append(tag.tag)

                result["tags"] = list_tags

            return Response(result, status=status.HTTP_200_OK)

        else:

            return Response(
                {"Permission Error": "This URL Not Created by this user"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

    def patch(self, request, pk):
        user_object = request.user
        url = request.data.get("url")
        title = request.data.get("title")
        category = request.data.get("category")
        tags = request.data.get("tags")

        user_url_object = get_object_or_404(UserURLModel, pk=pk)

        if user_url_object.user == user_object:
            result = {"user": user_object.username}
            # if payload have url key
            if url:
                url_object, _exists = URLModel.objects.get_or_create(
                    url=url, user=user_object
                )
                # if payload have title key
                if title:
                    url_object.title = title

                url_object.save()
                result["url"] = url_object.url
                result["title"] = url_object.title

                user_url_object.url = url_object

            # if payload have category key
            if category:
                category_object, _exists = CategoriesModel.objects.get_or_create(
                    category=category, user=user_object
                )
                category_object.save()
                result["category"] = category_object.category

                user_url_object.category = category_object

            # if payload have tags key
            if tags:
                list_tags = []
                for tag in tags:
                    tags_object, _exists = TagsModel.objects.get_or_create(
                        tag=tag, user=user_object
                    )
                    tags_object.save()
                    list_tags.append(tags_object.tag)

                    user_url_object.tags.add(tags_object)

                result["tags"] = list_tags

            user_url_object.save()
            return Response({"Update Sucessful": result}, status=status.HTTP_200_OK)

        else:

            return Response(
                {"Permission Error": "This URL Not Created by this user"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

    def delete(self, request, pk):
        user_object = request.user
        user_url_object = get_object_or_404(UserURLModel, pk=pk)
        if user_url_object.user == user_object:
            user_url_object.delete()
            user_url_object.save()
            return Response({"Deleted"}, status=status.HTTP_204_NO_CONTENT)
        else:

            return Response(
                {"Permission Error": "This URL Not Created by this user"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
