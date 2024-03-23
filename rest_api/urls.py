from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import fav_link, user

"""
    api/user[POST] -> create user

    api/favlink [GET] -> get all url already add by user
    api/favlink [POST] -> Create new Url 
    api/favlink [PUT] -> Update detail Url
    api/favlink [DELETE] -> Update detail Url

    api/favlink/category?name="?" [GET] -> get category name match with category created by user
    api/favlink/category [GET] -> get all category created by user
    api/favlink/category?name="?" [POST] -> Create New category relete with user 
    api/favlink/category [PUT] -> Update name  
    api/favlink/category?name="?" [DELETE] -> delete category   

    api/favlink/tag?name="?" [GET] -> get tag name match with tag created by user
    api/favlink/tag [GET] -> get all tag created by user
    api/favlink/tag?name="?" [POST] -> Create New tag relete with user 
    api/favlink/tag [PUT] -> Update name  
    api/favlink/tag?name="?" [DELETE] -> delete tag   
"""

router = format_suffix_patterns(
    [
        path(
            "api/user/",
            user.UserView.as_view(),
            name="user_registation_api",
        ),
        path("api/favlink/", fav_link.FavLinkView.as_view(), name="fav_link"),
        path(
            "api/favlink/<int:pk>/",
            fav_link.FavLinkViewById.as_view(),
            name="fav_link_by_id",
        ),
        # path("api/favlink/category", FavLinkView.as_view(), name="fav_link"),
        # path("api/favlink/tag", FavLinkView.as_view(), name="fav_link"),
    ]
)
urlpatterns = router
