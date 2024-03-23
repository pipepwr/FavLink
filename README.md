# FavLink
Rest Api for mange data of favorite url 

# RestAPI

## User Registration

### Request

`POST api/user `

### RESPONSE
{"message": "Create user Complete", 
"data":{"username":...,
        "password":...,
        "email",....}
}


    

## favlink

### Request

`GET api/favlink `

### RESPONSE
    {}
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


# CRON JOB

## REF

`https://medium.com/@mainadanielwachira/a-comprehensive-guide-to-using-django-crontab-for-scheduled-tasks-bb62b99083e8`

