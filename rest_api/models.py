from django.db import models
from django.contrib.auth.models import User
from http import HTTPStatus

"""
5 table [User, URL, Tags, Categories, UserURL]
First I Store Every Element on Dimension Table
And Create UserURL like Fact Tablel(Reference id from every table)
    - User is Default model from django
    - URL, Tags, Categories, UserURL, Contain ForeignKey "UserId" And When user deleted 
      those record on table should delete too.
    - Tags, Categories Can be delete. sperate with URL if user delete tag or categories
      UserUrl And URL Record Should still Avaiable.
** URL Can relate One Category
** URL Can relete many tags
** If user deleted every element deleted too.

Ref : https://docs.djangoproject.com/en/5.0/ref/models/fields/
"""


class URLModel(models.Model):
    url = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default="UnTitle")
    status_code = models.IntegerField(
        choices=[(s.value, s.name) for s in HTTPStatus], default=400
    )

    class Meta:
        unique_together = ("user", "url")


class TagsModel(models.Model):
    tag = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "tag")


class CategoriesModel(models.Model):
    category = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "category")


class UserURLModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.ForeignKey(URLModel, on_delete=models.CASCADE)
    category = models.ForeignKey(
        CategoriesModel, on_delete=models.SET_DEFAULT, default=None, null=True
    )
    tags = models.ManyToManyField(TagsModel)

    class Meta:
        unique_together = ("user", "url")
