from django_cloudspotlicense import PACKAGE_NAME
from .config import get_superuser_perm

def has_perm(user, perm):
    """ Returns True if user has the specified permission on the Cloudspot License server. """
    
    if user.has_perm(get_superuser_perm()):
        return True
    else:
        license_perm = '{0}.{1}'.format(PACKAGE_NAME, perm)
        return user.has_perm(license_perm)