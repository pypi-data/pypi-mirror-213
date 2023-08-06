# DRF SimpleJWT additions

Additional features for [django-rest-framework-simplejwt](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/index.html).
  
---
  
## Features
  
- [x] Full user info in TokenObtainPairSerializer
- [x] Full user info in TokenObtainPairView
- [x] Auto creation of user from token
  
---
  
## Installation
  
```bash
pip install drf-simplejwt-additions
```
  
---
  
## Usage

> Note: for all these features you need to set same `SECRET_KEY` and `SIMPLE_JWT['ALGORITHM']` in all services.
  
### Full user info in TokenObtainPairSerializer
  
In `settings.py`:
  
```python
INSTALLED_APPS = [
    ...
    'drf_simplejwt_additions',
    ...
]
  
...
  
SIMPLE_JWT = {
    ...
    "TOKEN_OBTAIN_SERIALIZER": "drf_simplejwt_additions.serializers.TokenObtainPairWithFullUserSerializer",
    ...
}
```
  
From now on, the response of the `TokenObtainPairView` will contain the full user info.  
Serializer get all fields from the user model.  
Then theses fields are added to the response in the `user` field.  

> User's password is also added to the response. But it's encrypted twice:
> - First time by Django itself
> - Second: JWT encryption
  
### Auto creation of user from token
  
This feature is useful in microservices architecture.
Token, obtained from one service, can be used in another service to get user info.
So, if the user doesn't exist in the second service, it will be created automatically.
  
In `settings.py`:
  
```python
INSTALLED_APPS = [
    ...
    'drf_simplejwt_additions',
    ...
]

...

MIDDLEWARE = [
    ...
    'drf_simplejwt_additions.middleware.AutoCreateUserFromTokenMiddleware',
    ...
]

...

REST_FRAMEWORK = {
    ...
    'DEFAULT_AUTHENTICATION_CLASSES': (
        ...
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        ...
    ),
    ...
}
```
  
> django-rest-framework-simplejwt has great feature: [TokenUserAuthentication](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/customizing_token_claims.html#tokenuserauthentication).
> But it doesn't create user automatically.
  
---
  
### Full user info in TokenObtainPairView
  
In `urls.py`:
  
```python
from drf_simplejwt_additions.views import TokenObtainPairWithFullUserView

urlpatterns = [
    ...
    path('api/token/', TokenObtainPairWithFullUserView.as_view(), name='token_obtain_pair'),
    ...
]
```
  
The `TokenObtainPairWithFullUserView` is a subclass of `TokenObtainPairView` with the `TokenObtainPairWithFullUserSerializer` serializer.
  
---
  
## License
  
[MIT](https://choosealicense.com/licenses/mit/)