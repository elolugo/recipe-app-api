from django.urls import path, include

from rest_framework.routers import DefaultRouter

from recipe import views

"""
Router -> Register/Associate URLs for a viewset.
For making easier for urlpatterns and path,
just including the router and therefore, all the urls registered on the router
"""
router = DefaultRouter()
router.register('tags', views.TagViewSet)

"""
Which app this urls.py belongs to.
This way reverse() function will find this urls
when using reverse(recipe:XXX)
"""
app_name = 'recipe'


urlpatterns = [
    path('', include(router.urls)),
]
