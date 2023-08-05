# django-cloudspotlicense
Django package to integrate the authentication of the Cloudspot License Server in other django applications.


## Getting started

### Install

Install with pip.

```python
pip install django-cloudspotlicense
```

### Quick start

1. Add ```django_cloudspotlicense``` to your INSTALLED_APPS

```python
INSTALLED_APPS = [
    ...
    'django_cloudspotlicense'
]
```

2. Include the URLConf in your project urls.py

```python
urlpatterns = [
    path('auth/', include('django_cloudspotlicense.urls')),
]
```

3. Run ``python manage.py migrate`` to create all the required models

4. Use the ```LoginView``` to let users log in using the Cloudspot License Server

```python
import django_cloudspotlicense.views as auth_views

urlpatterns = [
    path('login', auth_views.LoginView.as_view(), name='login')
]
```

A basic html template with no styling will be provided. You can overwrite this template by simply creating a new template at ```templates/auth/login.html```.
The only requirement for this template is that it includes two input elements with the name ```username``` and ```password```.

```html
<input type="text" name="username" />
<input type="password" name="password" />
```

5. Add the application ID as given by the Cloudspot License server to your ```settings.py```.

```python
# settings.py

CLOUDSPOT_LICENSE_APP = config('CLOUDSPOT_LICENSE_APP')
```

6. Done

## Setting up the User model

You can extend the User model as usual to add more attributes. ```django_cloudspotlicense``` also uses the User model to store additional information, such as tokens and the company id.
If you want to add additional attributes, import the User class from the package and add your attributes as usual.

```python
from django_cloudspotlicense.models import CloudspotUser

class User(CloudspotUser):
    extra_data = models.CharField(max_length=500, default='foobar')
```

Use as normal.

```python
print(user.extra_data) # foobar
```

## Permission checking

There are a few ways to check if the current user has the correct permission on the Cloudspot License server to do an action.
It's important that you **do not use the built-in permission checker from Django**. This will always return ```False``` on any given permission.

1. **Class-based views**

When using class-based views, you can import the modified ```PermissionRequiredMixin``` and ```LoginRequiredMixin```.
When using ```PermissionRequiredMixin```, the ```LoginRequiredMixin``` is implied as an anonymous user can not have any permissions.

```python
from django_cloudspotlicense.mixins import PermissionRequiredMixin, LoginRequiredMixin

# Use as is normal within Django
# The user needs the permission 'use_dashboard' to be able to view this template
class Dashboard(PermissionRequiredMixin, TemplateView):
    permission_required = 'use_dashboard' # use the permission code as shown in the Cloudspot License server
    template_name = '...'
# OR
# The user needs to be logged in and be assigned a company (which is always required) before he's able to see this view
class Projects(LoginRequiredMixin, TemplateView):
    template_name = '...'
```

2. **Functions**

You can use the utility function ```has_perm()``` to check if a user has a permission.

```python
from django_cloudspotlicense.utils import has_perm

if has_perm(user, 'use_dashboard'):
    # user has the permission use_dashboard in Cloudspot License server
else:
    # user does not have the permission
```

**! At this moment it's not possible to check multiple permissions at once. You will need to call the function for each permission.**

3. **Templates**

Inside a template, you can use a templatetag to check for the correct permission.

```html
<!-- This is REQUIRED, else the tag will not work -->
{% load license_tags %} 

<!-- Use the tag 'has_perm' on a user object -->
{% if request.user|has_perm:'list_projects' %}
    <!-- This piece of HTML will only be rendered if the user has the 'list_projects' permission -->
    <h3>Projects</h3>
    <ul>
        <li>...</li>
    </ul>
{% endif %}
```


## Webhook

This package also provides a webhook where the Cloudspot License Server will send updates to whenever the permissions for a user changes.
The webhook is located at ```https://example.com/auth/webhook```. This webhook is automatically activated when importing the URLConf.


## Migrating to the License server from an existing application

Migrating to the license server from an existing Django application that is using the local built-in user authentication is possible, but should be done with **extreme care** and careful consideration.
The following guide will step you through the required actions to succesfully migrate all the authentication to the license server.

**!! BACKUP YOUR DATABASE AND FILES BEFORE PROCEEDING**
Failure to follow the provided steps can result in breaking changes. Always have a backup ready.

### Setup
Copy the `merge_with_license_server.py` script located under `scripts` to your management commands directory in your Django project.

### 1. Add a new field 'backup_email' to the existing User model
This field will be used to copy the current username/email to, which will be needed later on. Be sure to allow null as it will be empty at first.

```python
# models.py

# THIS IS YOUR LOCAL USER MODEL
class User(AbstractUser):
    
    backup_email = models.CharField(max_length=500, null=True)
    # ...
```

### 2. Make migrations and migrate

```python
python manage.py makemigrations
python manage.py migrate
```

### 3. Run the first step of the migration script
This step will copy the existing username/email to the newly created `backup_email` field.

```python
python manage.py merge_with_license_server --step1
```

### 4. Install this package and add it to your INSTALLED_APPS

```python
pip install django-cloudspotlicense
```

```python
# settings.py

INSTALLED_APPS = [
    ...
    'django_cloudspotlicense'
]
```

### 5. Modify the existing User model
The existing User model should not inherit from `AbstractUser` anymore, but should be changed to a normal model at this point.

```python
# models.py

# THIS IS YOUR LOCAL USER MODEL
class User(models.Model): # WAS: class User(AbstractUser)
    # ...
```

Add the following fields at the top of the User model:

```python
# models.py

# THIS IS YOUR LOCAL USER MODEL
class User(models.Model): # WAS: class User(AbstractUser)
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'id'
    is_anonymous = False # can be either true or false, doesnt matter
    is_authenticated = True # can be either true or false, doesnt matter

    # ...
```

### 6. Make migrations and migrate

```python
python manage.py makemigrations
python manage.py migrate
```

### 7. Set AUTH_USER_MODEL in settings.py
Change the `AUTH_USER_MODEL` in your `settings.py` to `django_cloudspotlicense.CloudspotUser`.

```python
# settings.py

AUTH_USER_MODEL = 'django_cloudspotlicense.CloudspotUser'
```

### 8. Remove fields from existing User model and add new field
Remove the fields that we added in **step 5**.
Import the CloudspotUser and CloudspotCompany models and add a new field: `cloudspotuser_ptr` with a ForeignKey to CloudspotUser.

```python
# models.py
from django_cloudspotlicense.models import CloudspotUser, CloudspotCompany

# THIS IS YOUR LOCAL USER MODEL
class User(models.Model):

    cloudspotuser_ptr = models.ForeignKey(CloudspotUser, on_delete=models.SET_NULL, null=True)
```

### 9. Make migrations and migrate

```python
python manage.py makemigrations
python manage.py migrate
```

### 10. Run the second step of the migration script
This step will duplicate the existing users and companies to the newly created CloudspotUser and CloudspotCompany, preserving ID's and usernames.

**!! You may have to modify the script to import your local User and Company models**

```python
python manage.py merge_with_license_server --step2
```

### 11. Modify the existing User model again
Remove the `cloudspotuser_ptr` and `id` fields and let the User model inherit from `CloudspotUser`.
In this step you can also remove any other garbage fields that will not be used anymore.

```python
# models.py

# THIS IS YOUR LOCAL USER MODEL
class User(CloudspotUser):
    # ...
```

### 12. Make migrations and migrate
During `makemigrations`, you will have to provide a one-off default UUID for `cloudspotuser_ptr`. This UUID needs to be v4 but can be **any** UUID you like. This will not affect the existing data.
You can generate one here: https://www.uuidgenerator.net/

```python
python manage.py makemigrations # if asked, provide a one-off default for cloudspotuser_ptr and use a random UUIDv4
python manage.py migrate
```

### 13. Remove any other garbage fields
If there are any more garbage fields, you can delete them in this step and migrate again.

### 14. Set AUTH_USER_MODEL back to your local User model in settings.py
Change the `AUTH_USER_MODEL` again to point at your local User model.

```python
# settings.py

AUTH_USER_MODEL = 'main.User'
```

### 15. Migration done
The migration is now done. Follow the quick start from step 2.