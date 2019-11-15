from django.urls import path

from user import views


"""
Which app this urls.py belongs to.
This way reverse() function will find this urls
when using reverse(user:XXX)
"""
app_name = 'user'

"""
The name='create' is for reverse to work.
This way reverse() function will find this url
when using reverse(user:create)
"""
urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
]
