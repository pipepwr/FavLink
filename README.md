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
"""

## User Login

### Request

`POST api/user/login `

### PAYLOAD
    {username:...,
    password:...}
### RESPONSE
    {"message": "Login Complete"}
    

## FAVLINK

### Request

`GET api/favlink `
`POST api/favlink`
`PATCH api/favlink/<pk>`
`DELETE api/favlink/<pk>`

### RESPONSE
    Sucessful 

    {"message": "Sucessful", "data": result}

    False
   
    {"message": Error detail}


# CRON JOB

## REF

`https://medium.com/@mainadanielwachira/a-comprehensive-guide-to-using-django-crontab-for-scheduled-tasks-bb62b99083e8`

