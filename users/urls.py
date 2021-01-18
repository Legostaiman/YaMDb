from django.urls import path

from .views import Users, UserDetail, SignUp, AboutMe, get_token

urlpatterns = [

    path('api/v1/users/me/', AboutMe.as_view(), name='about_me'),
    path('api/v1/users/', Users.as_view()),
    path('api/v1/users/<str:username>/', UserDetail.as_view()),
    path('api/v1/auth/email/', SignUp.as_view(), name='confirmation_code'),
    path('api/v1/auth/token/', get_token, name='token_obtain_pair'),

]
