from django_cloudspotlicense import PACKAGE_NAME

ROOT_PERM='use_app'
SUPERUSER_PERM='is_superuser'

def get_root_perm():
    return f'{PACKAGE_NAME}.{ROOT_PERM}'

def get_superuser_perm():
    return f'{PACKAGE_NAME}.{SUPERUSER_PERM}'