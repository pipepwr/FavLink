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
"""""""""""""""""""""""""""

## User Login

### Request

`POST api/user/login `

### PAYLOAD
    {username:...,
    password:...}
### RESPONSE
    {"message": "Login Complete"}

"""""""""""""""""""""""""""

## FAVLINK

### Request

`GET api/favlink `
`DELETE api/favlink/<pk>`
`GET api/favlink/<pk>/tag/<tag_id>`
`GET api/favlink/<pk>/category`
`DELETE api/favlink/<pk>/tag/<tag_id>`
`DELETE api/favlink/<pk>/category`

### RESPONSE
    Sucessful 

    {"message": "Sucessful", "data": result}

    False
   
    {"message": Error detail}

"""""""""""""""""""""""""""
### Create or update FAVLINK

`POST api/favlink`
`PATCH api/favlink/<pk>`

### PAYLOAD
    {
        "url": "https://test.com/",
        "category": "categorytest",
        "tags": [
            "test",
            "fly",
            "moo"
        ]
    }
    **** category, tags is Optionals for PATCH

### RESPONSE
    {
    "message": "Querry Sucessfull",
    "data": {
        "id": ..,
        "url": "https://test.com/",
        "title": "test - เข้าสู่ระบบหรือสมัครใช้งาน",
        "category": "categorytest",
        "tags": [
            "test",
            "fly",
            "moo"
        ]
        }
    }


"""""""""""""""""""""""""""

## TAG, Category

### Reqest

`GET api/{tag, category}`
`POST api/{tag, category}`
`PATCH api/{tag, category}/<pk>`
`DELETE api/{tag, category}/<pk>`


### RESPONSE
    {
    message : ["Sucessful", "Error"]
    tag_data : {
                    "id": tag.id,
                    "tag_name": tag_object.tag,
                    "urls": list_url,
                }
    }
"""""""""""""""""""""""""""
# CRON JOB

## URL Validity Check

    Run url_valid_check in job.py EveryMidnight
    You can set time in attr `CRONJOBS` in settings.py file

`https://medium.com/@mainadanielwachira/a-comprehensive-guide-to-using-django-crontab-for-scheduled-tasks-bb62b99083e8`

