# DRF SimpleJWT additions

Additional features for [django-rest-framework-simplejwt](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/index.html).
  
---
  
## Features
  
- [x] Full user info in TokenObtainPairSerializer
- [x] Full user info in TokenObtainPairView
  
---
  
## Installation
  
```bash
pip install drf-simplejwt-additions
```
  
---
  
## Usage
  
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
Serializer get all fields from the user model, except `password` and fields that start with `_`.  
Then theses fields are added to the response in the `user` field.
  
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