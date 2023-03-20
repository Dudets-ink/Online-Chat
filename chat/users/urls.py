from django.urls import path

from .views import Logout, SignIn, SignUp

urlpatterns = [
    path('logout/', Logout, name='logout'),
    path('sign_in/', SignIn.as_view(), name='sign_in'),
    path('sign_up/', SignUp.as_view(), name='sign_up'),
]
