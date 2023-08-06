# Django Custom Users App
  
App that provides custom user model for Django projects.
You don't need to create your own app for users in every project.
  
This app itself might not be useful. It's just a template for creating custom user model.  
You can use it as a starting point for your own app.  
E.g. you can fork this repo, customize it and push to your own repo.  
Then you can install it in your projects using `pip install <your-repo-url>`.
  
> If you find this app useful, please consider giving it a star on [GitHub](https://github.com/AllYouZombies/django-custom-users-app).
  
---
  
## Installation
  
```shell
pip install django-custom-users-app
```
  
---
  
## Usage
  
Add `users` to `INSTALLED_APPS` in your `settings.py` file.
  
```python
INSTALLED_APPS = [
    ...
    'users',
    ...
]
```
  
Add `AUTH_USER_MODEL` to your `settings.py` file.
  
```python
AUTH_USER_MODEL = 'users.User'
```
  
Then run migrations:
  
```shell
python manage.py migrate
```
  
---
  
## License
  
[MIT](https://choosealicense.com/licenses/mit/)
  
---
  