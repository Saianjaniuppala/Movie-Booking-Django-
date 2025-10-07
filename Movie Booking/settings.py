INSTALLED_APPS += [
'rest_framework',
'rest_framework.authtoken',
'drf_yasg',
'movies',
]


REST_FRAMEWORK = {
'DEFAULT_AUTHENTICATION_CLASSES': (
'rest_framework_simplejwt.authentication.JWTAuthentication',
),
'DEFAULT_PERMISSION_CLASSES': (
'rest_framework.permissions.IsAuthenticatedOrReadOnly',
),
}


from datetime import timedelta
SIMPLE_JWT = {
'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
'AUTH_HEADER_TYPES': ('Bearer',),
}
